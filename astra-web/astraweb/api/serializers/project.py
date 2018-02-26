from rest_framework import serializers
from api.models.project import Project
from api.models.devices import Device
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectIDSerializer(serializers.ModelSerializer):
    id_error = {'failure': 'Project does not exist'}

    def exists(self):
        self.is_valid()
        return ('pk' in self.data) and (Project.objects.filter(
            pk=self.data['pk']).exists())

    class Meta:
        model = Project
        fields = (
            'pk'
        )

