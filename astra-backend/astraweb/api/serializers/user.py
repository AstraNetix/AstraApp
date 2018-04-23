from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models.device import Device
from api.models.project import Project
from api.exceptions.user_exceptions import CreationError, AuthenticationError, ReferralError
from api.sales.promo_sale import PromoSale

User = get_user_model()

class UserIdentification(serializers.Serializer):
    """
    A base class meant for verifying user existence, with only basic serialization
    incorporated. Has no fields so not meant to be exposed as an endpoint.
    """
    email_error = {'email': ['Email does not exist.']}

    def exists(self):
        self.is_valid()
        return ('email' in self.data) and User.objects.filter(
            email=self.data['email']).exists()

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


class UserRegisterSerializer(UserIdentification):
    """
    Used for creating users.
    """
    name                    =   serializers.CharField(max_length=200, allow_blank=True, required=False)
    email                   =   serializers.EmailField(max_length=None, min_length=None)
    password                =   serializers.CharField(max_length=200, min_length=6, write_only=True)
    confirm_password        =   serializers.CharField(max_length=200, min_length=6, write_only=True)
    telegram_addr           =   serializers.CharField(allow_blank=True, required=False)
    ether_addr              =   serializers.CharField(allow_blank=True, required=False, max_length=42, min_length=42)
    user_type               =   serializers.ChoiceField(choices=list(User.USER_TYPE_CHOICES), allow_blank=True, required=False)

    def create(self, validated_data):
        if User.objects.filter(email=validated_data["email"]).exists():
            raise CreationError.user_exists()
        if validated_data["password"] != validated_data.pop("confirm_password"):
            raise CreationError.unmatching_passwords()
        name = [name.title() for name in validated_data.pop('name').split(" ")]
        
        if len(name) == 3:
            first_name, middle_name, last_name = name
        elif len(name) == 2 and name[1]:
            first_name, last_name = name
            middle_name = None
        else: 
            first_name, middle_name, last_name = name[0], None, None
            
        user = User.objects.create_user(
            first_name=first_name, 
            middle_name=middle_name, 
            last_name=last_name, 
            **validated_data,
        )
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
        user = User.objects.get(email=validated_data["email"])
        name = validated_data.pop("name", False)
        new_password = validated_data.pop("new_password", False)
        new_email = validated_data.pop("new_email", False)

        if name:
            name = [field.title() for field in name.split(" ")]
            if len(name) == 3:
                user.first_name, user.middle_name, user.last_name = name
            elif len(name) == 2 and name[1]:
                user.first_name, user.last_name = name
            else: 
                user.first_name = name[0]
            user.save()

        if new_password:
            if "old_password" not in validated_data:
                raise CreationError.old_password_required()
            user = User.authenticate(email=validated_data["email"], password=validated_data["old_password"])
            if new_password != validated_data.pop("confirm_password", ""):
                raise CreationError.unmatching_passwords()
            user.set_password(validated_data["new_password"])
            user.save()

        if new_email:
            user.email = User.objects.normalize_email(new_email)
            user.save()
            
        return user

class UserICOKYCSerializer(UserIdentification):
    """
    Used for inputting ICO KYC information for users.
    """
    email               =   serializers.EmailField()
    first_name          =   serializers.CharField(max_length=50, required=False, allow_blank=True)
    middle_name         =   serializers.CharField(max_length=50, required=False, allow_blank=True)
    last_name           =   serializers.CharField(max_length=50, required=False, allow_blank=True)
    street_addr1        =   serializers.CharField(max_length=100, required=False, allow_blank=True)
    street_addr2        =   serializers.CharField(max_length=100, required=False, allow_blank=True)
    city                =   serializers.CharField(max_length=40, required=False, allow_blank=True)
    state               =   serializers.CharField(min_length=2, required=False, allow_blank=True)
    country             =   serializers.CharField(min_length=2, max_length=2, required=False, allow_blank=True)
    zip_code            =   serializers.IntegerField(required=False, allow_null=True)
    phone_number        =   serializers.CharField(max_length=150, required=False, allow_blank=True)
    ether_addr          =   serializers.CharField(max_length=42, min_length=42, required=False, allow_blank=True)
    ether_part_amount   =   serializers.IntegerField(required=False, allow_null=True)
    referral_type       =   serializers.ChoiceField(choices=User.REFERRAL_CHOICES, required=False, allow_blank=True)
    referral_code       =   serializers.CharField(required=False, allow_blank=True)
    whitepaper          =   serializers.BooleanField(required=False)
    token_sale          =   serializers.BooleanField(required=False)
    data_protection     =   serializers.BooleanField(required=False)


    def add_icokyc(self):
        user = User.objects.get(email=self.data.pop('email'))
        
        self.check_errors = {}
        for key, value in self.data.items(): 
            if (key == 'country' and value == '00') or (key == 'referral_code'):
                continue 
            if key in ['whitepaper', 'token_sale', 'data_protection']:
                setattr(user, key, True if value == '1' else False)
            if key == 'ether_addr' and value and len(value) != 42:
                self.check_errors['ether_addr'] = ['This field must be a 42 character hex value']
            setattr(user, key, value)
        user.save()

        PromoSale.make_referee(user, self.data.pop('referral_code', ''))
        PromoSale.complete_whitelist(user)


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
