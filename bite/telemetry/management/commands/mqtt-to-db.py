import socket
import asyncio
import json
import time
import paho.mqtt.client as mqtt
from asgiref.sync import sync_to_async
from asyncio_mqtt import Client

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from api.models import Device
from telemetry.models import Telemetry

MQTT_HOST = settings.MQTT_BROKER['HOST']
MQTT_PORT = int(settings.MQTT_BROKER['PORT'])


class Command(BaseCommand):
    help = 'MQTT to DB deamon'

    @sync_to_async
    def get_device(self, serial):
        try:
            return Device.objects.get(serial=serial)
        except ObjectDoesNotExist:
            return None

    @sync_to_async
    def store_telemetry(self, device, payload):
        Telemetry.objects.create(
            device=device,
            transport='mqtt',
            clock=payload['clock'],
            payload=payload['payload']
        )

    async def mqtt_broker(self):
        async with Client(MQTT_HOST, port=MQTT_PORT) as client:
            # use shared subscription for HA/balancing
            await client.subscribe("$share/telemetry/#")
            async with client.unfiltered_messages() as messages:
                async for message in messages:
                    payload = json.loads(message.payload.decode('utf-8'))
                    device = await self.get_device(message.topic)
                    if device is not None:
                        await self.store_telemetry(device, payload)
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                'DEBUG: message discarded'))

    def handle(self, *args, **options):
        client = mqtt.Client()
        while True:
            try:
                client.connect(MQTT_HOST, MQTT_PORT)
                break
            except (socket.gaierror, ConnectionRefusedError):
                self.stdout.write(
                    self.style.WARNING('WARNING: Broker not available'))
                time.sleep(5)

        self.stdout.write(self.style.SUCCESS('INFO: Broker subscribed'))
        client.disconnect()
        asyncio.run(self.mqtt_broker())
