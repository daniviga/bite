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
        fields = ('time', 'device', 'clock', 'transport', 'payload',)
        read_only_fields = ['transport']

    def create(self, validated_data):
        validated_data['transport'] = 'http'
        telemetry = Telemetry.objects.create(**validated_data)
        return telemetry
