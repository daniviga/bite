# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# BITE - A Basic/IoT/Example
# Copyright (C) 2020 Daniele Viganò <daniele@vigano.me>
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
import paho.mqtt.client as mqtt
from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceUnavailable

from django.conf import settings

MQTT_HOST = settings.MQTT_BROKER['HOST']
MQTT_PORT = int(settings.MQTT_BROKER['PORT'])


class MQTTHealthCheck(BaseHealthCheckBackend):
    critical_service = True

    def check_status(self):
        client = mqtt.Client(client_id="django-hc")
        try:
            client.connect(MQTT_HOST, port=MQTT_PORT)
            client.disconnect()
        except (socket.gaierror, ConnectionRefusedError):
            self.add_error(ServiceUnavailable("Connection refused"))

    def identifier(self):
        return self.__class__.__name__
