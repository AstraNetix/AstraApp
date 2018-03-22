from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models.device import Device
from api.models.project import Project
from api.exceptions.user_exceptions import CreationError, AuthenticationError

User = get_user_model()


class UserIdentificationSerializer(serializers.ModelSerializer):
    email_error = {'failure': 'Email does not exist'}

    def exists(self):
        self.is_valid()
        return ('email' in self.data) and (User.objects.filter(
            email=self.data['email']).exists())

    class Meta:
        model = User
        fields = (
            'email',
        )   
        
class UserLoginSerializer(UserIdentificationSerializer):
    class Meta:
        model = User
        extra_kwargs = {
            'password': {'write_only': True},   
        }
        fields = (
            'email',
            'password',
        )
        
class UserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=200, min_length=6)
    new_password = serializers.CharField(max_length=200, min_length=6)

    class Meta:
        model = User
        extra_kwargs = {
            'new_password': {'write_only': True},
            'old_password': {'write_only': True},
        }
        fields = (
            'email',
            'old_password'
            'new_password',
        )

class UserBasicSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')
    confirm_password = serializers.CharField(max_length=200)

    def create(self, validated_data):
        if User.objects.filter(email=validated_data["email"]).exists():
            raise CreationError.user_exists()
        if validated_data["password"] != validated_data["confirm_password"]:
            raise CreationError.unmatching_passwords()
        user = User.objects.create(**validated_data)

        try:
            user.first_name, user.last_name = user.first_name.split(" ")
        except ValueError:  # If for some reason, user only gave first name
            user.first_name = user.first_name

        user.validate_email()
        user.save()
        return user

    class Meta:
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }
        fields = (
            'name', 
            'email',
            'password',
            'confirm_password',
            'telegram_addr'
            'ether_addr', 
        )

class UserUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')
    old_password = serializers.CharField(max_length=200)
    new_password = serializers.CharField(max_length=200)
    confirm_password = serializers.CharField(max_length=200)

    def update(self, validated_data):
        user = User.authenticate(email=validated_data["email"], password=validated_data["old_password"])
        if validated_data["new_password"] != validated_data["confirm_password"]:
            raise CreationError.unmatching_passwords()
        try:
            user.first_name, user.last_name = validated_data["name"].split(" ")
        except ValueError:  # If for some reason, user only gave first name
            user.first_name = user.first_name

        user.email = validated_data["email"]
        user.save()
        return user

    class Meta:
        model = User
        extra_kwargs = {
            'old_password': {'write_only': True},
            'new_password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }
        fields = (
            'name', 
            'email',
            'old_password',
            'old_password',
            'confirm_password',
        )

class UserICOKYCSerializer(UserIdentificationSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'street_addr1',  
            'street_addr2',
            'city', 
            'state',  
            'country',  
            'zip_code',
            'phone_number', 
            'ether_addr',
            'id_file', 
            'selfie',  
            'ether_part_amount', 
            'referral',
        )

class UserAirDropsSerializer(UserIdentificationSerializer):
    class Meta:
        model = User
        fields = (
            'telegram_addr',
            'twitter_name',
            'facebook_url',
            'linkedin_url',
            'bitcoin_name',
            'reddit_name',
            'steemit_name',
            'referral', 
        )

class UserBalanceSerializer(UserIdentificationSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'bitcoin_balance', 
            'ether_balance', 
            'usd_balance', 
            'star_balance',
        )

class UserRelationalSerializer(UserIdentificationSerializer):
    email_error = {'failure': 'User does not exist'}
    device_id_error = {'failure': 'Device does not exist'}
    project_id_error = {'failure': 'Project does not exist'}

    def exists(self):
        self.is_valid()

        if not ('email' in self.data) or not (User.objects.filter(
            email=self.data['email']).exists()):
            self.errors = self.email_error
            return False

        if not ('device-pk' in self.data) or not (Device.objects.filter(
            pk=self.data['device-pk']).exists()):
            self.errors = self.device_id_error
            return False

        if not ('project-pk' in self.data) or not (Project.objects.filter(
            pk=self.data['project-pk']).exists()):
            self.errors = self.project_id_error
            return False

        return True


    class Meta:
        model = Project
        fields = (
            'email',
            'device-pk',
            'project-pk'
            )
