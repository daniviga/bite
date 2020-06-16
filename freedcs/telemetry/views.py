from datetime import datetime
from django.http import Http404
from rest_framework.viewsets import ModelViewSet

from telemetry.models import Telemetry
from telemetry.serializers import TelemetrySerializer
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


class TelemetryRange(ModelViewSet):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer
    lookup_field = 'device'

    def list(self, request, device, time_from, time_to=None):
        queryset = Telemetry.objects.filter(
            device__serial=device,
            time__range=[time_from, datetime.now()])
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
            device__serial=device).order_by('-time')
        if not queryset:
            raise Http404
        serializer = TelemetrySerializer(queryset[0])
        return Response(serializer.data)
