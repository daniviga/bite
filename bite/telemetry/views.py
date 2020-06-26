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

from datetime import datetime
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from telemetry.models import Telemetry
from telemetry.serializers import (TelemetrySerializer,
                                   TelemetrySummarySerializer)
from rest_framework.response import Response


class TelemetryView(ModelViewSet):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer
    lookup_field = 'device'

    def list(self, request, device=None):
        queryset = Telemetry.objects.filter(device__serial=device)
        if not queryset:
            raise Http404
        serializer = TelemetrySerializer(queryset, many=True)
        return Response(serializer.data)


class TelemetrySummaryView(APIView):
    def get(self, request, device, format=None):
        count = Telemetry.objects.filter(device__serial=device).count()
        if count == 0:
            raise Http404
        first = Telemetry.objects.filter(
            device__serial=device).order_by('-time')[:1][0]
        last = Telemetry.objects.filter(
            device__serial=device).order_by('time')[:1][0]
        data = {
            'device': device,
            'stats': {
                'count_samples': count,
                'first_sample': first.time,
                'last_sample': last.time}
        }
        serializer = TelemetrySummarySerializer(data)
        return Response(serializer.data)


class TelemetryRange(ModelViewSet):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer
    lookup_field = 'device'

    def list(self, request, device, time_from, time_to=None):
        time_to = datetime.now() if time_to is None else time_to
        queryset = Telemetry.objects.filter(
            device__serial=device,
            time__range=[time_from, time_to])
        if not queryset:
            raise Http404
        serializer = TelemetrySerializer(queryset, many=True)
        return Response(serializer.data)


class TelemetryLatest(ModelViewSet):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer
    lookup_field = 'device'

    def retrieve(self, request, device=None):
        queryset = Telemetry.objects.filter(
            device__serial=device).order_by('-time')[:1]
        if not queryset:
            raise Http404
        serializer = TelemetrySerializer(queryset[0])
        return Response(serializer.data)
