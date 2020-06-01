from rest_framework.viewsets import ModelViewSet

from telemetry.models import Telemetry
from telemetry.serializers import TelemetrySerializer


class Telemetry(ModelViewSet):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer

    # def post(self, request):
    #     serializer = DeviceSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request):
    #     devices = Device.objects.all()
    #     import pdb; pdb.set_trace()
    #     serializer = DeviceSerializer(devices)
    #     return Response(serializer.serial)
