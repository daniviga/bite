from django.http import Http404
from rest_framework.viewsets import ModelViewSet

from telemetry.models import Telemetry
from telemetry.serializers import TelemetrySerializer
from rest_framework.response import Response


class TelemetryView(ModelViewSet):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer

    def list(self, request, device=None):
        queryset = Telemetry.objects.filter(device__serial=device)
        if not queryset:
            raise Http404
        serializer = TelemetrySerializer(queryset, many=True)
        return Response(serializer.data)
