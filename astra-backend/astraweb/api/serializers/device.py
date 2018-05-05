from rest_framework import serializers
from api.models.device import Device
from api.exceptions.device_exceptions import DeviceIDError
from django.contrib.auth import get_user_model
User = get_user_model()

class DeviceIDSerializer(serializers.ModelSerializer):
    id_error = {'failure': ['Device does not exist']}

    def exists(self):
        self.is_valid()
        if (('id' in self.data) and 
            (Device.objects.filter(uid=self.data['id']).exists()) and 
            ('email' in self.data)):
            user = User.objects.filter(email=self.data['email'])
            if user == Device.objects.get(uid=self.data['id']).user: 
                return True
            raise DeviceIDError.ownership_error()
        else:
            raise DeviceIDError.does_not_exist()

    class Meta:
        model = Device
        fields = (
            'uid'
        )

class DeviceCreateSerializer(serializers.ModelSerializer):
    id_error = {'failure': ['User does not exist']}

    def exists(self):
        self.is_valid()
        return ('email' in self.data) and (User.objects.filter(
            email=self.data['email']).exists())

    email = serializers.CharField(max_length=200)
    class Meta:
        model = Device
        fields = (
            'email',
            'name', 
            'company', 
            'model', 
            )

class DeviceUsageSerializer(DeviceIDSerializer):
    class Meta: 
        model = Device
        fields = (
            'email',
            'uid',
            'run_on_batteries',
            'run_if_active',
            'max_CPUs',
            'disk_max_percent',
            'ram_max_percent',
            'cpu_max_percent',
        )