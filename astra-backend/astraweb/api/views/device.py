from api.models.device import Device
from django.contrib.auth import get_user_model
from api.serializers.device import (
    DeviceCreateSerializer,
    DeviceIDSerializer,
    DeviceUsageSerializer,
    )

from api.permissions import APIUserPermission

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status

from rest_framework.decorators import detail_route, list_route  
from rest_framework.response import Response

from api.exceptions.device_exceptions import DeviceIDError

User = get_user_model()

class DeviceIDViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceIDSerializer

    queryset = Device.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, APIUserPermission]

    dicter = lambda model, attrs: {attr: getattr(model, attr) for attr in attrs}

    @list_route(methods=['patch'])
    def quit(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        try: 
            serializer.exists()
            return Response({
                
            }, status=status.HTTP_200_OK)
        except DeviceIDError as die:
            return Response({'failure': die.errors}, 
                    status=status.HTTP_412_PRECONDITION_FAILED)

    @list_route(methods=['patch'])
    def store_data(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        try: 
            serializer.exists()
            device = Device.objects.get(uid=serializer.data['uid'])
            return Response({
                'info'          :   self.dicter(device, ['name', 'model', 'processor', 'graphics', 'memory']),
                'projects'      :   {
                                    **{proj.url: [proj.name, True] for proj in device.active_projects}
                                    **{proj.url: [proj.name, False] for proj in device.dormant_projects}
                                    },
                'preferences'   :   self.dicter(device, ['run_on_batteries', 'run_if_active', 'use_mem_only']),
                'limits'        :   self.dicter(device, ['max_CPUs', 'disk_max_percent', 'ram_max_percent', 
                                        'cpu_max_percent', 'net_max_bytes_up', 'net_max_bytes_down']),
                'times'         :   self.dicter(device, ['mon_start', 'mon_end', 'tues_start', 'tues_end', 'wed_start', 
                                        'wed_end', 'thurs_start', 'thurs_end', 'fri_start', 'fri_end', 'sat_start', 
                                        'sat_end', 'sun_start', 'sun_end']),
                'fine_data'     :   self.dicter(device.usage, ['cpu_fine', 'gpu_fine', 'disk_fine', 'network_fine']),
                'coarse_data'   :   self.dicter(device.usage, ['cpu_coarse', 'gpu_coarse', 'disk_coarse', 'network_coarse']),
            }, status=status.HTTP_200_OK)
        except DeviceIDError as die:
            return Response({'failure': die.errors}, 
                    status=status.HTTP_412_PRECONDITION_FAILED)    

    @list_route(methods=['patch'])
    def info(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.exists()
            device = Device.objects.get(uid=serializer.data['uid'])
            return Response(self.dicter(device, ['name', 'model', 'processor', 'graphics', 'memory']), 
                status=status.HTTP_200_OK)
        except DeviceIDError as die:
            return Response({'failure': die.errors}, 
                    status=status.HTTP_412_PRECONDITION_FAILED)

    @list_route(methods=['patch'])
    def data(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.exists()
            device = Device.objects.get(uid=serializer.data['uid'])
            return Response({
                    **self.dicter(device.usage, ['cpu_fine', 'gpu_fine', 'disk_fine', 'network_fine']),
                    **self.dicter(device.usage, ['cpu_coarse', 'gpu_coarse', 'disk_coarse', 'network_coarse'])
                }, status=status.HTTP_200_OK)
        except DeviceIDError as die:
            return Response({'failure': die.errors}, 
                    status=status.HTTP_412_PRECONDITION_FAILED)

    @list_route(methods=['patch'])
    def projects(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.exists()
            device = Device.objects.get(uid=serializer.data['uid'])
            return Response({
                    **{proj.url: [proj.name, True] for proj in device.active_projects}
                    **{proj.url: [proj.name, False] for proj in device.dormant_projects}
                }, status=status.HTTP_200_OK)
        except DeviceIDError as die:
            return Response({'failure': die.errors}, 
                    status=status.HTTP_412_PRECONDITION_FAILED)

class DeviceCreateViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceCreateSerializer

    queryset = Device.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, APIUserPermission]

    @list_route(methods=['patch'])
    def create(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        
        try:  
            serializer.exists()
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
        except DeviceIDError as die:
            return Response({'failure': die.errors}, 
                    status=status.HTTP_412_PRECONDITION_FAILED)

class DeviceUsageViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceUsageSerializer

    queryset = Device.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, APIUserPermission]

    @list_route(methods=['patch'])
    def config_hours(self, request, pk=None):
        def worker(device, serializer):
            for day in serializer.data['days']:
                setattr(device, Device.DAY_MAP[day] + '_start', 
                    serializer.data['start-hour'])
                setattr(device, Device.DAY_MAP[day] + '_end', 
                    serializer.data['end-hour'])
            Device.pubnub.publish(message={
                'function': 'config-hours',
                'days': serializer.data['days'],
                'start-hour': serializer.data['start-hour'],
                'end-hour': serializer.data['end-hour']
            })
        return self._usage_parser(request, worker)

    @list_route(methods=['patch'])
    def run_on_batteries(self, request, pk=None):
        def worker(device, serializer):
            device.run_on_batteries = serializer.data['run-on-batteries']
            Device.pubnub.publish(message={
                'function': 'run-on-batteries',
                'opt': serializer.data['run-on-batteries'],
            })
        return self._usage_parser(request, worker)

    @list_route(methods=['patch'])
    def run_if_active(self, request, pk=None):
        def worker(device, serializer):
            device.run_if_active = serializer.data['value']
            Device.pubnub.publish(message={
                'function': 'run-if-active',
                'opt': serializer.data['run-if-active'],
            })
        return self._usage_parser(request, worker)
    
    @list_route(methods=['patch'])
    def run_on_batteries(self, request, pk=None):
        def worker(device, serializer):
            device.run_on_batteries = serializer.data['value']
            Device.pubnub.publish(message={
                'function': 'run-on-batteries',
                'opt': serializer.data['run-on-batteries'],
            })
        return self._usage_parser(request, worker)
    
    @list_route(methods=['patch'])
    def use_memory_only(self, request, pk=None):
        def worker(device, serializer):
            device.run_on_batteries = serializer.data['value']
            Device.pubnub.publish(message={
                'function': 'use-memory-only',
                'opt': serializer.data['run-on-batteries'],
            })
        return self._usage_parser(request, worker)

    @list_route(methods=['patch'])
    def cpu_percent(self, request, pk=None):
        def worker(device, serializer):
            device.cpu_max_percent = serializer.data['percent']
            Device.pubnub.publish(message={
                'function': 'cpu-percent',
                'percent': serializer.data['percent'],
            })
        return self._usage_parser(request, worker)
    
    @list_route(methods=['patch'])
    def max_cpus(self, request, pk=None):
        def worker(device, serializer):
            device.run_if_active = serializer.data['max_cpus']
            Device.pubnub.publish(message={
                'function': 'max-cpus',
                'number': serializer.data['max_cpus'],
            })
        return self._usage_parser(request, worker)
    
    @list_route(methods=['patch'])
    def disk_percent(self, request, pk=None):
        def worker(device, serializer):
            device.disk_max_percent = serializer.data['percent']
            Device.pubnub.publish(message={
                'function': 'disk-percent',
                'percent': serializer.data['percent'],
            })
        return self._usage_parser(request, worker)
    
    @list_route(methods=['patch'])
    def ram_percent(self, request, pk=None):
        def worker(device, serializer):
            device.ram_max_percent = serializer.data['percent']
            Device.pubnub.publish(message={
                'function': 'ram-percent',
                'percent': serializer.data['percent'],
            })
        return self._usage_parser(request, worker)

    @list_route(methods=['patch'])
    def network_down(self, request, pk=None):
        def worker(device, serializer):
            device.net_max_bytes_down = serializer.data['kbps']
            Device.pubnub.publish(message={
                'function': 'network-down',
                'kbps': serializer.data['kbps'],
            })
        return self._usage_parser(request, worker)

    @list_route(methods=['patch'])
    def network_up(self, request, pk=None):
        def worker(device, serializer):
            device.net_max_bytes_up = serializer.data['kbps']
            Device.pubnub.publish(message={
                'function': 'network-up',
                'kbps': serializer.data['kbps'],
            })
        return self._usage_parser(request, worker)

    @list_route(methods=['patch'])
    def resource_usage(self, request, pk=None):
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
        return self._usage_parser(request, worker)

    def _usage_parser(self, request, worker):
        serializer = self.serializer_class(data=request.data)
        try: 
            serializer.exists()
            device = Device.objects.get(uid=serializer.data['uid'])
            worker(device, serializer)
            return Response({'success': 'Usage limit set.'}, status=status.HTTP_200_OK)
        except DeviceIDError as die:
            return Response({'failure': die.errors}, 
                    status=status.HTTP_412_PRECONDITION_FAILED)