from rest_framework import serializers
from api.models.device import Device
from api.exceptions.device_exceptions import DeviceIDError
from django.contrib.auth import get_user_model
User = get_user_model()

class DeviceIDSerializer(serializers.ModelSerializer):
    id_error = {'failure': ['Device does not exist']}

    def exists(self):
        self.is_valid()
        return ('id' in self.data) and (Device.objects.filter(
            uid=self.data['id']).exists())

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
    def exists(self):
        exist = super().exists() and ('email' in self.data) 
        if exist:
            user = User.objects.filter(email=self.data['email'])
            if user == Device.objects.get(uid=self.data['id']).user: 
                return True
            raise DeviceIDError.ownership_error()
        else:
            raise DeviceIDError.does_not_exist()

    class Meta: 
        model = Device
        fields = (
            'email',
            'uid',
            'run_on_batteries',
            'run_if_active',
            'start_hour',
            'end_hour',
            'max_CPUs',
            'disk_max_percent',
            'ram_max_percent',
            'cpu_max_percent',
        )