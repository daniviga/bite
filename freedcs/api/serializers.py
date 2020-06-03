from rest_framework import serializers
from api.models import Device, device_validation


class DeviceSerializer(serializers.ModelSerializer):
    serial = serializers.CharField(
        max_length=128,
        validators=[device_validation],
    )  # disable unique validation

    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ('creation_time', 'updated_time')

    def create(self, validated_data):
        device, created = Device.objects.update_or_create(
            serial=validated_data['serial'],
            defaults={'serial': validated_data['serial']},
        )
        return device
