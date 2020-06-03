from rest_framework import serializers
from api.models import Device
from telemetry.models import Telemetry


class TelemetrySerializer(serializers.ModelSerializer):
    device = serializers.SlugRelatedField(
        slug_field='serial',
        queryset=Device.objects.all()
    )

    class Meta:
        model = Telemetry
        fields = ('time', 'device', 'clock', 'payload',)
