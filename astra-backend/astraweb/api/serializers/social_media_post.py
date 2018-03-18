import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models.social_media_post import SocialMediaPost
from api.models.user_exceptions import AuthenticationError

User = get_user_model()

class SocialMediaPostIDSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    str_date = serializers.CharField(max_length=23)
    class Meta:
        model = SocialMediaPost
        fields = (
            'email',
            'str_date',
        )  

class SocialMediaPostCreateSerializer(serializers.ModelSerializer):
    @staticmethod
    def convert_date(str_date):
        return datetime.datetime(
                year=str_date[0:4], 
                month=str_date[5:7], 
                day=str_date[8:10], 
                hour=str_date[11:13], 
                minute=str_date[15:17],
                second=str_date[19:21],
        )

    def create(self, validated_data):
        user = User.objects.get(email=validated_data.pop('email'))
        if not user.exists():
            raise AuthenticationError.user_does_not_exist()

        # Date must be a string in RfC 3339 format
        str_date = validated_data.pop('str_date', False)
        date = self.convert_date(str_date) if str_date else datetime.datetime.utcnow()
        
        post = SocialMediaPost.objects.create(user=user, date=date, **validated_data)
        post.save()
        return post

    class Meta:
        model = SocialMediaPost
        fields = (
            'platform',
            'content',
            'email',
            'str_date',
        )  

