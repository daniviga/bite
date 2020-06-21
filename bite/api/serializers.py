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
