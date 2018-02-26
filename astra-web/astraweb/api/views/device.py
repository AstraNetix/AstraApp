from api.models.device import Device
from django.contrib.auth import get_user_model
from api.serializers.device import (
    DeviceCreateSerializer,
    DeviceIDSerializer
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