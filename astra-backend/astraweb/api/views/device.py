from api.models.device import Device
from django.contrib.auth import get_user_model
from api.serializers.device import (
    DeviceCreateSerializer,
    DeviceIDSerializer,
    DeviceUsageSerializer,
    )

from api.permissions import SuperUserPermission

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status

from rest_framework.decorators import detail_route, list_route  
from rest_framework.response import Response

User = get_user_model()

class DeviceIDViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceCreateSerializer

    queryset = Device.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserPermission]

    def create(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.exists():
            user = User.objects.get(email=serializer.data['user-email'])
            device = Device.objects.create_device(
                name=serializer.data['name'], 
                company=serializer.data['company'], 
                model=serializer.data['model'],
                user=user
            )
            device.save()
            return Response({'success': "Device created"}, 
                status=status.HTTP_200_OK)
        else: 
            return Response(serializer.id_error, 
                status=status.HTTP_400_BAD_REQUEST)
    
    def quit(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.exists():
            device = Device.objects.get(uid=serializer.data['id'])
            device.active = False
            Device.pubnub.publish(message={'function': 'quit'})
            return Response({'success': 'Usage limit set.'}, status=status.HTTP_200_OK)
        else:
            return Response({'failure': serializer.error}, 
                    status=status.HTTP_412_PRECONDITION_FAILED)

class DeviceUsageViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceUsageSerializer

    queryset = Device.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserPermission]

    @list_route(methods=['patch'])
    def config_hours(self, request, pk=None):
        def worker(device, serializer):
            device.start_hour = serializer.data['start-hour']
            device.end_hour = serializer.data['end-hour']
            Device.pubnub.publish(message={
                'function': 'config-hours',
                'start': serializer.data['start-hour'],
                'end': serializer.data['end-hour']
                })
        return usage_parser(request, worker)

    
    @list_route(methods=['patch'])
    def set_run_on_batteries(self, request, pk=None):
        def worker(device, serializer):
            device.run_on_batteries = serializer.data['run-on-batteries']
            Device.pubnub.publish(message={
                'function': 'run-on-batteries',
                'opt': serializer.data['run-on-batteries'],
                })
        return usage_parser(request, worker)

    @list_route(methods=['patch'])
    def set_run_if_active(self, request, pk=None):
        def worker(device, serializer):
            device.run_if_active = serializer.data['run-if-active']
            Device.pubnub.publish(message={
                'function': 'run-if-active',
                'opt': serializer.data['run-if-active'],
                })
        return usage_parser(request, worker)

    @list_route(methods=['patch'])
    def set_max_cpus(self, request, pk=None):
        def worker(device, serializer):
            device.run_if_active = serializer.data['max_cpus']
            Device.pubnub.publish(message={
                'function': 'max-cpus',
                'number': serializer.data['max_cpus'],
                })

    @list_route(methods=['patch'])
    def set_resource_usage(self, request, pk=None):
        def worker(device, serializer):
            if 'disk-max-percent' in serializer.data:
                device.disk_max_percent = serializer.data['disk-max-percent']
                Device.pubnub.publish(message={
                    'function': 'disk-percent',
                    'percent': serializer.data['disk-max-percent'],
                })
            if 'ram-max-usage' in serializer.data:
                device.ram_max_usage = serializer.data['ram-max-usage']
                Device.pubnub.publish(message={
                    'function': 'ram-percent',
                    'percent': serializer.data['ram-max-percent'],
                })
            if 'cpu-max-usage' in serializer.data:
                device.cpu_max_usage = serializer.data['cpu-max-usage']
                Device.pubnub.publish(message={
                    'function': 'cpu-percent',
                    'percent': serializer.data['cpu-max-percent'],
                })       
        return usage_parser(request, worker)

    def usage_parser(self, request, helper):
        serializer = self.serializer_class(data=request.data)
        if serializer.exists():
            device = Device.objects.get(uid=serializer.data['id'])
            worker(device, serializer)
            return Response({'success': 'Usage limit set.'}, status=status.HTTP_200_OK)
        else:
            return Response({'failure': serializer.error}, 
                    status=status.HTTP_412_PRECONDITION_FAILED)