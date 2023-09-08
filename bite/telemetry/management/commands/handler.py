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

import json
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from api.models import Device
from telemetry.models import Telemetry


class Command(BaseCommand):
    help = 'MQTT to DB deamon'

    KAFKA_HOST = settings.KAFKA_BROKER['HOST']
    KAFKA_PORT = int(settings.KAFKA_BROKER['PORT'])

    def get_device(self, serial):
        try:
            return Device.objects.get(serial=serial)
        except ObjectDoesNotExist:
            return None

    def store_telemetry(self, transport, message):
        Telemetry.objects.create(
            transport=transport,
            device=self.get_device(message["device"]),
            clock=message["clock"],
            payload=message["payload"]
        )

    def handle(self, *args, **options):
        while True:
            try:
                consumer = KafkaConsumer(
                    "telemetry",
                    bootstrap_servers='{}:{}'.format(
                        self.KAFKA_HOST, self.KAFKA_PORT
                    ),
                    group_id="handler",
                    value_deserializer=lambda m: json.loads(m.decode('utf8')),
                )
                break
            except NoBrokersAvailable:
                self.stdout.write(
                    self.style.WARNING('WARNING: Kafka broker not available'))
                time.sleep(5)

        self.stdout.write(self.style.SUCCESS('INFO: Kafka broker subscribed'))
        for message in consumer:
            self.store_telemetry(
                message.value["transport"],
                message.value["body"]
            )
        consumer.unsuscribe()
