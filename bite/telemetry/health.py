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
