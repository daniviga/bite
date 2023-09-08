# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# BITE - A Basic/IoT/Example
# Copyright (C) 2020-2021 Daniele Viganò <daniele@vigano.me>
#
# BITE is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BITE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socket
import asyncio
import json
import time
import paho.mqtt.client as mqtt
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from asgiref.sync import sync_to_async
from aiomqtt import Client

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from api.models import Device


class Command(BaseCommand):
    help = 'MQTT to DB deamon'

    MQTT_HOST = settings.MQTT_BROKER['HOST']
    MQTT_PORT = int(settings.MQTT_BROKER['PORT'])
    KAFKA_HOST = settings.KAFKA_BROKER['HOST']
    KAFKA_PORT = int(settings.KAFKA_BROKER['PORT'])
    producer = None

    @sync_to_async
    def get_device(self, serial):
        try:
            return Device.objects.get(serial=serial)
        except ObjectDoesNotExist:
            return None

    @sync_to_async
    def dispatch(self, message):
        self.producer.send(
            'telemetry', {"transport": 'mqtt',
                          "body": message}
        )

    async def mqtt_broker(self):
        async with Client(self.MQTT_HOST, port=self.MQTT_PORT) as client:
            # use shared subscription for HA/balancing
            await client.subscribe("$share/telemetry/#")
            async with client.messages() as messages:
                async for message in messages:
                    device = await self.get_device(message.topic)
                    if device is not None:
                        message_body = json.loads(
                            message.payload.decode('utf-8'))
                        await self.dispatch(message_body)
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                'DEBUG: message discarded'))

    def handle(self, *args, **options):
        client = mqtt.Client()
        while True:
            try:
                client.connect(self.MQTT_HOST, self.MQTT_PORT)
                break
            except (socket.gaierror, ConnectionRefusedError):
                self.stdout.write(
                    self.style.WARNING('WARNING: MQTT broker not available'))
                time.sleep(5)

        while True:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers='{}:{}'.format(
                        self.KAFKA_HOST, self.KAFKA_PORT
                    ),
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    retries=5
                )
                break
            except NoBrokersAvailable:
                self.stdout.write(
                    self.style.WARNING('WARNING: Kafka broker not available'))
                time.sleep(5)

        self.stdout.write(self.style.SUCCESS('INFO: Brokers subscribed'))
        client.disconnect()
        asyncio.run(self.mqtt_broker())
