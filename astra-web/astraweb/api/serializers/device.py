from rest_framework import serializers
from api.models.device import Device
from django.contrib.auth import get_user_model
User = get_user_model()

class DeviceIDSerializer(serializers.ModelSerializer):
    id_error = {'failure': 'Device does not exist'}

    def exists(self):
        self.is_valid()
        return ('pk' in self.data) and (Device.objects.filter(
            uid=self.data['pk']).exists())

    class Meta:
        model = Device
        fields = (
            'uid'
        )

class DeviceCreateSerializer(serializers.ModelSerializer):
    id_error = {'failure': 'User does not exist'}

    def exists(self):
        self.is_valid()
        return ('user-email' in self.data) and (User.objects.filter(
            email=self.data['user-email']).exists())

    user_email = serializers.CharField(max_length=200)
    class Meta:
        model = Device
        fields = (
            'user_email',
            'name', 
            'company', 
            'model', 
            )