import sys
from rest_framework import serializers

from api.models.social_media_post import SocialMediaPost
from api.models.email import Email
from api.models.file import File
from api.models.project import Project
from api.models.usage import Data
from api.models.device import Device

from django.contrib.auth import get_user_model
User = get_user_model()

MODEL_MAPPING = {
                    'email':        Email,
                    'file':         File,
                    'project':      Project,
                    'data':         Data,
                    'device':       Device,
                    'social_media': SocialMediaPost,
                    'user':         User,
                }

MODEL_CHOICES = ((model, model.title()) for model in MODEL_MAPPING.keys())

class PrioritySerializer(serializers.Serializer):
    item            =   serializers.CharField()
    priority        =   serializers.IntegerField(min_value=0)

class QuerySerializer(serializers.Serializer):
    model           =   serializers.ChoiceField(choices=MODEL_CHOICES)
    priorities      =   PrioritySerializer(many=True)
    max_level       =   serializers.IntegerField(min_value=0, default=sys.maxsize)

    def searcher(self, item, level=0):
        if level > self.validated_data['max_level']:
            return False

        
        