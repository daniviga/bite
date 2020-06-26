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
from api.models import Device
from telemetry.models import Telemetry


class TelemetryStatsSerializer(serializers.Serializer):
    count_samples = serializers.IntegerField()
    first_sample = serializers.DateTimeField()
    last_sample = serializers.DateTimeField()


class TelemetrySummarySerializer(serializers.Serializer):
    device = serializers.CharField()
    stats = TelemetryStatsSerializer()


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
