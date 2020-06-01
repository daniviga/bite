from rest_framework import serializers
from api.models import Device, WhiteList


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('serial', 'creation_time', 'updated_time',)


# class WhiteListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Device
#         fields = ('serial', 'creation_time', 'updated_time',)
