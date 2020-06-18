from django.apps import AppConfig
from health_check.plugins import plugin_dir


class TelemetryConfig(AppConfig):
    name = 'telemetry'

    def ready(self):
        from telemetry.health import MQTTHealthCheck
        plugin_dir.register(MQTTHealthCheck)
