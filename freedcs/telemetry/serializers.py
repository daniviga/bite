from rest_framework import serializers
from api.serializers import DeviceSerializer
from telemetry.models import Telemetry


class TelemetrySerializer(serializers.ModelSerializer):
    # device = DeviceSerializer(read_only=True)

    def validate(self, data):
        return data

    class Meta:
        model = Telemetry
        fields = ('time', 'device', 'clock', 'payload',)


# class WhiteListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Device
#         fields = ('serial', 'creation_time', 'updated_time',)
