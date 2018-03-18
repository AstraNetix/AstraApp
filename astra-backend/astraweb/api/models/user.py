from __future__ import unicode_literals
import uuid
import re

from django.db import models
from django.contrib.auth import authenticate as auth
from django.contrib.auth.models import AbstractUser, BaseUserManager

from api.models.project import Project

from api.models.user_exceptions import AuthenticationError, PasswordChangeError, TokenICOKYCError

from django.core.validators import RegexValidator
from django.core.mail import send_mail

from phonenumber_field.modelfields import PhoneNumberField
from passlib.context import CryptContext


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(User.pwd_context.hash(password))
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)




class User(AbstractUser):

    #######################################################################################
    # Meta Options

    class Meta:
        app_label       =   "api"
        db_table        =   "api_user"

    NONE                =   0
    INVESTOR            =   1
    CONTRIBUTOR         =   2
    BOTH                =   3

    USER_TYPE_CHOICES   =   (
                                (NONE, 'none'),
                                (INVESTOR, 'investor'),
                                (CONTRIBUTOR, 'contributor'),
                                (BOTH, 'both'),
                            )

    app_header          =   "https://www.goastra.info/" # Add web app url header here

    verbose_name        =   'user'
    verbose_name_plural =   'users'

    objects             =   UserManager()

    USERNAME_FIELD      =   'email'
    REQUIRED_FIELDS     =   []

    pwd_context = CryptContext(
        schemes=["pbkdf2_sha256", "des_crypt"],
        deprecated="auto",
    )

    #######################################################################################
    # Fields

    logged_in           =   models.BooleanField('logged_in', default=False)

    username            =   None
    email               =   models.EmailField(('email address'), unique=True)
    first_name          =   models.CharField(max_length=50)
    middle_name         =   models.CharField(max_length=150, blank=True, null=True)
    last_name           =   models.CharField(max_length=150, blank=True, null=True)
    phone_number        =   PhoneNumberField(null=True, blank=True)

    is_active           =   models.BooleanField('active', default=True)
    is_staff            =   models.BooleanField('staff', default=False)
    is_superuser        =   models.BooleanField('superuser', default=False)

    street_addr1         =   models.CharField(max_length=100, null=True, blank=True)
    street_addr2         =   models.CharField(max_length=100, null=True, blank=True)
    city                =   models.CharField(max_length=40, null=True, blank=True)
    state               =   models.CharField(validators=[RegexValidator(
                                regex='^\w{2}$', 
                                message='State ID length must be 2 characters', 
                                code='nomatch'
                            )],
                            max_length=2, null=True,  blank=True)
    country             =   models.CharField(validators=[RegexValidator(
                                regex='^\w{2}$', 
                                message='Country code length must be 2 characters', 
                                code='nomatch'
                            )],
                            max_length=50, null=True, blank=True)
    zip_code            =   models.PositiveIntegerField(null=True, blank=True)
    id_file             =   models.ImageField(null=True, blank=True)
    selfie              =   models.ImageField(upload_to="./selfies", null=True, blank=True)
    ether_addr          =   models.CharField(
                            validators=[RegexValidator(
                                regex='^\w{40}$', 
                                message='Ether address length must be 40 characters', 
                                code='nomatch'
                            )], 
                            max_length=40, null=True, blank=True
                            )
    ether_part_amount   =   models.PositiveIntegerField(null=True, blank=True)
    telegram_addr       =   models.CharField(max_length=50, blank=True, null=True)

    bitcoin_balance     =   models.DecimalField(max_digits=11, decimal_places=4, default=0)
    ether_balance       =   models.DecimalField(max_digits=11, decimal_places=4, default=0)
    usd_balance         =   models.DecimalField(max_digits=11, decimal_places=2, default=0)
    star_balance        =   models.DecimalField(max_digits=11, decimal_places=2, default=0)

    start_time          =   models.DateField(auto_now_add=True, editable=False)

    user_type           =   models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=NONE)
    
    projects            =   models.ManyToManyField(Project, blank=True)

    email_verified      =   models.BooleanField(blank=True, default=False)
    phone_verified      =   models.BooleanField(blank=True, default=False)

    twitter_name        =   models.CharField(max_length=50, blank=True, null=True)
    facebook_url        =   models.URLField(blank=True, null=True)
    linkedin_url        =   models.URLField(blank=True, null=True)
    bitcoin_name        =   models.CharField(max_length=50, blank=True, null=True)
    reddit_name         =   models.CharField(max_length=50, blank=True, null=True)
    steemit_name        =   models.CharField(max_length=50, blank=True, null=True)
    
    referral            =   models.EmailField(null=True, blank=True)


    def __str__(self):
        return self.first_name if self.first_name else "" + " " + self.last_name if self.last_name else ""

    def get_full_name(self):
        return self.__str__()

    def get_short_name(self):
        return self.first_name if self.first_name else ""


    #######################################################################################
    # Contacting User

    def send_email(self, subject, message):
        """
        Sends an email to this user using the current STMP email
        middleware, with the subject and message inputed.
        """
        send_mail(
            subject = subject, 
            message = message, 
            from_email = "noreply@mail.goastra.win", 
            recipient_list = [self.email], 
            fail_silently = True
        )
        return True

    def send_sms(self, message):
        """
        Sends an SMS to this user using the current STMP email
        middleware, with the message inputed.
        """
        send_mail(
            subject = '', 
            message = message, 
            from_email = "noreply@mail.goastra.win", 
            recipient_list = [self.phone_number], 
            fail_silently = True
        )
        return True

    def validate_email(self):
        return self.send_email(
            "Activate Astra",
            ("{0},\n\n"
            "Welcome to Astra! Please click the following link to "
            "confirm your email address for Astra\n\n"
            "{1}\n\n"
            "After you do so, remember to fill out the rest of your ICO-"
            "KYC form to begin token sale.\n\n"
            "Best,\n\n"
            "The Astra Team ").format(self.first_name, "") #TODO: Add email confirmation link
        )

    def remind_validate_email(self):
        return self.send_email(
            "Reminder to Activate Astra",
            ("{0},\n\n"
            "Hi! We're emailing you again to remind you to "
            "confirm your email address for Astra\n\n"
            "{1}\n\n"
            "After you do so, remember to fill out the rest of your ICO-"
            "KYC form to begin token sale.\n\n"
            "Best,\n\n"
            "The Astra Team ").format(self.first_name, "") #TODO: Add email confirmation link
        )

    def reset_password_email(self):
        return self.send_email(
            "Reset Password",
            ("{0},\n\n"
            "Hi! Please click the following link to reset your password\n\n"
            "{1}/login/forgot-password\n\n"
            "If you believe you have gotten this email in error, please ignore this message.\n\n"
            "Best,\n\n"
            "The Astra Team ").format(self.first_name, self.app_header) 
        )

    def validate_phone(self):
        return self.send_sms(
            "Welcome to Astra, {0}!. Please click the following link to "
            "confirm your phone number\n\n" 
            "{1}\n\n"
            "After you do so, remember to fill out the rest of your ICO-"
            "KYC form to begin token sale.".format(self.first_name, "") #TODO: Add phone confirmation link
        )

    def set_email_valid(self):
        self.email_verified = True

        if self.user_type == self.NONE:
            self.user_type = self.CONTRIBUTOR
        elif self.user_type == self.INVESTOR:
            self.user_type = self.BOTH

        self.save()

    def set_email_invalid(self):
        self.email_verified = False

        if self.user_type == self.CONTRIBUTOR:
            self.user_type = self.NONE
        elif self.user_type == self.BOTH:
            self.user_type = self.INVESTOR

        self.save()

    def set_phone_valid(self):
        self.phone_verified = True
        self.save()

    #######################################################################################
    # Token sale

    @staticmethod
    def add_star_tokens(user, amount):
        user.token_auth()
        user.star_balance += amount
        user.save()

    @staticmethod
    def add_usd(user, amount):  
        user.token_auth()
        user.usd_balance += amount
        user.save()

    @staticmethod
    def add_bitcoin(user, amount):
        user.token_auth()
        user.bitcoin_balance += amount
        user.save()

    @staticmethod
    def add_ether(user, amount):
        user.token_auth()
        user.ether_balance += amount
        user.save()

    #######################################################################################
    # Passwords

    def change_password(self, old_password, new_password):
        """
        Confirms user's old password to be old_password and changes
        it to new_password.
        """
        valid_regex = "^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$"
        if not (old_password and new_password):
            PasswordChangeError.missing_fields()
        if len(new_password) < 6:
            PasswordChangeError.password_too_short()
        if not re.match(valid_regex, new_password):
            PasswordChangeError.invalid_characters()
        if not self.check_password(old_password):
            PasswordChangeError.incorrect_password()

        self.set_password(new_password)
        self.save()

    def reset_password(self, new_password):
        """
        Reset's user password to new_password. Only to be done after 
        email confirmation.
        """
        valid_regex = "^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$"
        if len(new_password) < 6:
            PasswordChangeError.password_too_short()
        if not re.match(valid_regex, new_password):
            PasswordChangeError.invalid_characters()

        self.set_password(new_password) 
        self.save()

    #######################################################################################
    # Authentication

    def valid_for_sale(self):
        """
        Checks to see if user has submitted all ICO-KYC form 
        data.
        """
        return all([
            self.street_addr, 
            self.city, 
            self.state, 
            self.country, 
            self.zip_code,
            self.id_file, 
            self.selfie,
            self.ether_addr, 
            self.ether_part_amount,
        ])

    def token_auth(self):
        """
        If a user is currently valid for token sale; must have email 
        verified, must be currently active, and must have filled 
        ICO-KYC form.
        """
        if not self.email_verified:
            raise TokenICOKYCError.not_verified()
        if not self.is_active:
            raise TokenICOKYCError.inactive()
        if not self.valid_for_sale():
            raise TokenICOKYCError.incomplete_ICO()

    def boolean_token_auth(self):
        """
        Boolean, non-error raising version of the previous function
        """
        return (
            self.email_verified and 
            self.is_active and 
            self.valid_for_sale()
            )

    @staticmethod
    def authenticate(email, password):
        """
        Attempt to authenticate a user, given a email and
        password. Return the user or raise AuthenticationError.
        """
        if not (email and password):
            raise AuthenticationError.missing_fields()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist: 
            raise AuthenticationError.user_does_not_exist()
        if not user or User.pwd_context.verify(user.password, password):
            raise AuthenticationError.invalid_credentials()
        if not user.is_active:
            raise AuthenticationError.inactive_account()
        return user

    def login(self):
        """ 
        Logs in a user. Only to be used after authentication
        """
        self.logged_in = True

    #######################################################################################
    # Transactions (PyEthApp Abstractions)

    def send_funds(self, value):
        tx = eth.transact(self.ether_addr, value=value)
        return eth.find_transaction(tx)
        

    #######################################################################################
    # Sales

    ### Make calls to SALE model to check for eligibility, change token value, etc. based on
    ### start date, current date, etc.
        