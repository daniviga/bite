from rest_framework.viewsets import ModelViewSet

from api.models import Device
from api.serializers import DeviceSerializer


class APISubscribe(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

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
