from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models.device import Device
from api.models.project import Project
from api.exceptions.user_exceptions import CreationError, AuthenticationError

User = get_user_model()

class UserIdentification(serializers.Serializer):
    """
    A base class meant for verifying user existence, with only basic serialization
    incorporated. Has no fields so not meant to be exposed as an endpoint.
    """
    email_error = {'failure': 'Email does not exist'}

    def exists(self):
        self.is_valid()
        return ('email' in self.data) and (User.objects.filter(
            email=self.data['email']).exists())

class UserIdentificationSerializer(serializers.ModelSerializer, UserIdentification):
    """
    A base class that verifies users but extends Model Serializer with a single 
    email field.
    """
    class Meta:
        model = User
        fields = (
            'email',
        )   
        
class UserLoginSerializer(UserIdentificationSerializer):
    """
    Used for logging in users.
    """
    class Meta:
        model = User
        extra_kwargs = {
            'password'      :   {'write_only': True},   
        }
        fields = (
            'email',
            'password',
        )
        
class UserPasswordSerializer(UserIdentification):
    """
    Used for changing users' passwords.
    """
    email                   =   serializers.EmailField(allow_blank=False)
    old_password            =   serializers.CharField(max_length=200, min_length=6, write_only=True, required=False, allow_blank=True)
    new_password            =   serializers.CharField(max_length=200, min_length=6, write_only=True)


class UserBasicSerializer(UserIdentification):
    """
    Used for creating users and getting basic user information.
    """
    name                    =   serializers.CharField(max_length=200)
    email                   =   serializers.EmailField(max_length=None, min_length=None)
    password                =   serializers.CharField(max_length=200, min_length=6, write_only=True)
    confirm_password        =   serializers.CharField(max_length=200, min_length=6, write_only=True)
    telegram_addr           =   serializers.CharField(allow_blank=True, required=False)
    ether_addr              =   serializers.CharField(allow_blank=True, required=False, max_length=40, min_length=40)

    def create(self, validated_data):
        if User.objects.filter(email=validated_data["email"]).exists():
            raise CreationError.user_exists()
        if validated_data["password"] != validated_data.pop("confirm_password"):
            raise CreationError.unmatching_passwords()
        name = validated_data.pop('name')
        try:
            first_name, last_name = name.split(" ")
        except ValueError:  # If for some reason, user only gave first name
            first_name, last_name = name, None
        user = User.objects.create_user(first_name=first_name, last_name=last_name, **validated_data)

        # user.validate_email() TODO uncomment this
        user.save()
        return user

class UserUpdateSerializer(UserIdentification):
    """
    Used for updating basic user information.
    """
    email               =   serializers.EmailField()
    name                =   serializers.CharField(max_length=200, required=False, allow_blank=True)
    new_email           =   serializers.EmailField(required=False, allow_blank=True)
    old_password        =   serializers.CharField(max_length=200, write_only=True, required=False, allow_blank=True)
    new_password        =   serializers.CharField(max_length=200, write_only=True, required=False, allow_blank=True)
    confirm_password    =   serializers.CharField(max_length=200, write_only=True, required=False, allow_blank=True)

    def update(self, validated_data):
        user = User.authenticate(email=validated_data["email"], password=validated_data["old_password"])
        if "new_password" in validated_data and "old_password" not in validated_data:
            raise CreationError.old_password_required()
        elif (("new_password" in validated_data and "confirm_password" not in validated_data) 
            or (validated_data["new_password"] != validated_data["confirm_password"])):
            raise CreationError.unmatching_passwords()

        try:
            user.first_name, user.last_name = validated_data["name"].split(" ")
        except ValueError:  # If for some reason, user only gave first name
            user.first_name = validated_data["name"]

        user.email = User.objects.normalize_email(validated_data["new_email"])
        user.set_password(validated_data["new_password"])
        
        user.save()
        return user

class UserICOKYCSerializer(UserIdentificationSerializer):
    """
    Used for getting ICO KYC information for users.
    """
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
    """
    Used for getting social media information for users.
    """
    class Meta:
        model = User
        fields = (
            'email',
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
    """
    Used for getting user balances.
    """
    class Meta:
        model = User
        fields = (
            'email',
            'bitcoin_balance', 
            'ether_balance', 
            'usd_balance', 
            'star_balance',
        )

class UserRelationalSerializer(UserIdentification):
    """
    Used for starting and stopping projects.
    """

    # TODO Change to using regular serializer instead of model serializer OR THIS WON'T WORK

    email_error         =   {'failure'  : 'User does not exist'}
    device_id_error     =   {'failure'  : 'Device does not exist'}
    project_id_error    =   {'failure'  : 'Project does not exist'}

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
            'project-pk',
            )
