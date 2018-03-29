import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models.social_media_post import SocialMediaPost
from api.exceptions.user_exceptions import AuthenticationError

User = get_user_model()

class SocialMediaPostIDSerializer(serializers.Serializer):
    email               =   serializers.EmailField(max_length=200)
    str_date            =   serializers.CharField(min_length=20)

class SocialMediaPostCreateSerializer(SocialMediaPostIDSerializer):
    platform            =   serializers.CharField(max_length=2)
    content             =   serializers.CharField()

    @staticmethod
    def convert_date(str_date):
        return datetime.datetime(
                year=int(str_date[0:4]), 
                month=int(str_date[5:7]), 
                day=int(str_date[8:10]), 
                hour=int(str_date[11:13]), 
                minute=int(str_date[14:16]),
                second=int(str_date[17:19]),
        )

    def create(self):
        try:
            user = User.objects.get(email=self.validated_data.pop('email'))
        except User.DoesNotExist:
            raise AuthenticationError.user_does_not_exist()

        # Date must be a string in RFC 3339 format
        str_date = self.validated_data.pop('str_date', False)
        date = self.convert_date(str_date) if str_date else datetime.datetime.utcnow()
    
        post = SocialMediaPost(user=user, date=date, **self.validated_data)
        post.uid = post.hash_code()
        post.save()
        return post


