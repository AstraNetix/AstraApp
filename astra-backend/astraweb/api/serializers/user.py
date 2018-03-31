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
    email_error = {'email': ['Email does not exist.']}

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
    name                    =   serializers.CharField(max_length=200, allow_blank=True, required=False)
    email                   =   serializers.EmailField(max_length=None, min_length=None)
    password                =   serializers.CharField(max_length=200, min_length=6, write_only=True)
    confirm_password        =   serializers.CharField(max_length=200, min_length=6, write_only=True)
    telegram_addr           =   serializers.CharField(allow_blank=True, required=False)
    ether_addr              =   serializers.CharField(allow_blank=True, required=False, max_length=40, min_length=40)
    user_type               =   serializers.ChoiceField(choices=list(User.USER_TYPE_CHOICES))

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

class UserICOKYCSerializer(UserIdentification):
    """
    Used for inputting ICO KYC information for users.
    """
    email               =   serializers.EmailField(required=True)
    first_name          =   serializers.CharField(max_length=50, required=False, allow_blank=True)
    middle_name         =   serializers.CharField(max_length=50, required=False, allow_blank=True)
    last_name           =   serializers.CharField(max_length=50, required=False, allow_blank=True)
    street_addr1        =   serializers.CharField(max_length=100, required=False, allow_blank=True)
    street_addr1        =   serializers.CharField(max_length=100, required=False, allow_blank=True)
    city                =   serializers.CharField(max_length=40, required=False, allow_blank=True)
    state               =   serializers.CharField(min_length=2, max_length=2, required=False, allow_blank=True)
    country             =   serializers.CharField(min_length=2, max_length=2, required=False, allow_blank=True)
    zip_code            =   serializers.IntegerField(required=False, allow_null=True)
    phone_number        =   serializers.CharField(required=False, allow_blank=True)
    ether_addr          =   serializers.CharField(max_length=40, min_length=40, required=False, allow_blank=True)
    id_file             =   serializers.ImageField(allow_empty_file=True, required=False)
    selfie              =   serializers.ImageField(allow_empty_file=True, required=False)
    ether_part_amount   =   serializers.IntegerField(required=False, allow_null=True)
    referral            =   serializers.EmailField(required=False, allow_blank=True)


class UserAirDropsSerializer(UserIdentification):
    """
    Used for inputting social media information for users.
    """
    email               =   serializers.EmailField(required=True)
    telegram_addr       =   serializers.CharField(max_length=50, required=False, allow_blank=True)
    twitter_name        =   serializers.CharField(max_length=50, required=False, allow_blank=True)
    facebook_url        =   serializers.CharField(required=False, allow_blank=True)
    linkedin_url        =   serializers.CharField(required=False, allow_blank=True)
    bitcoin_name        =   serializers.CharField(max_length=50, required=False, allow_blank=True)
    reddit_name         =   serializers.CharField(max_length=50, required=False, allow_blank=True)
    steemit_name        =   serializers.CharField(max_length=50, required=False, allow_blank=True)
    referral            =   serializers.EmailField(required=False, allow_blank=True)


class UserBalanceSerializer(UserIdentification):
    """
    Used for changing user balances.
    """
    email               =   serializers.EmailField(required=True)
    bitcoin             =   serializers.DecimalField(max_digits=11, decimal_places=4, required=False, allow_null=True)
    ether               =   serializers.DecimalField(max_digits=11, decimal_places=4, required=False, allow_null=True)
    usd                 =   serializers.DecimalField(max_digits=11, decimal_places=2, required=False, allow_null=True)
    star                =   serializers.DecimalField(max_digits=11, decimal_places=2, required=False, allow_null=True)


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
