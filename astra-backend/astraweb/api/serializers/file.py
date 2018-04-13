from rest_framework import serializers
from api.models.file import File
from django.contrib.auth import get_user_model

User = get_user_model()

class FileUploadSerializer(serializers.Serializer):
    email = serializers.EmailField()
    datafile = serializers.FileField()
    filetype = serializers.ChoiceField(choices=File.FILE_TYPES)

    def exists(self):
        return (
            self.is_valid() and 
            'email' in self.validated_data and 
            User.objects.filter(email=self.validated_data['email']).exists()
        )

    def create(self, validated_data):
        user = User.objects.get(email=validated_data.pop('email'))
        new_file = File.objects.create(user=user, **validated_data)
        new_file.save()
        return new_file