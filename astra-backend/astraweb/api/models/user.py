from __future__ import unicode_literals
import uuid
import re
import random
import string
import itertools
from decimal import Decimal

from django.db import models
from django.contrib.auth import authenticate as auth
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import check_password

from api.exceptions.user_exceptions import AuthenticationError, PasswordChangeError, TokenICOKYCError, ReferralError

from django.core.validators import RegexValidator, MinValueValidator
from django.core.mail import send_mail, send_mass_mail

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
        user.set_password(password)
        user.set_referral_code(email)
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
        extra_fields.setdefault('is_api_user', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_api_user') is not True:
            raise ValueError('Superuser must have is_api_user=True.')

        return self._create_user(email, password, **extra_fields)
    
    def create_api_user(self, email, password, **extra_fields):
        """
        Create and save an API user with given email and password
        """
        extra_fields.setdefault('is_api_user', True)

        if extra_fields.get('is_api_user') is not True:
            raise ValueError('API user must have is_api_user=True.')

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
                                (NONE,          'None'          ),
                                (INVESTOR,      'Investor'      ),
                                (CONTRIBUTOR,   'Contributor'   ),
                                (BOTH,          'Both'          ),
                            )
    
    NO_REFERRAL         =   0
    GOOGLE              =   1
    EMAIL               =   2
    FACEBOOK            =   3
    REFERRAL            =   4

    REFERRAL_CHOICES    =   (
                                (NO_REFERRAL,   'No Referral'       ),
                                (GOOGLE,        'Google'            ),
                                (EMAIL,         'Email Marketing'   ),
                                (FACEBOOK,      'Facebook'          ),
                                (REFERRAL,      'Referral'          ),
                            )

    WEB_HEADER          =   "http://goastra.tinyewebswirl.com/" 
    APP_HEADER          =   ""

    verbose_name        =   'user'
    verbose_name_plural =   'users'

    objects             =   UserManager()

    USERNAME_FIELD      =   'email'
    REQUIRED_FIELDS     =   []


    #######################################################################################
    # Fields

    logged_in           =   models.BooleanField('logged_in', default=False)
    username            =   models.CharField(max_length=1, default='0')

    email               =   models.EmailField(('email address'), unique=True)
    first_name          =   models.CharField(max_length=50)
    middle_name         =   models.CharField(max_length=150, blank=True, null=True)
    last_name           =   models.CharField(max_length=150, blank=True, null=True)
    phone_number        =   models.CharField(max_length=150, blank=True, null=True)

    is_active           =   models.BooleanField('active', default=True)
    is_staff            =   models.BooleanField('staff', default=False)
    is_superuser        =   models.BooleanField('superuser', default=False)
    is_api_user         =   models.BooleanField('api_user', default=False)

    street_addr1        =   models.CharField(max_length=100, null=True, blank=True)
    street_addr2        =   models.CharField(max_length=100, null=True, blank=True)
    city                =   models.CharField(max_length=40, null=True, blank=True)
    state               =   models.CharField(max_length=200, null=True,  blank=True)
    country             =   models.CharField(validators=[RegexValidator(
                                regex='^\w{2}$', 
                                message='State ID length must be 2 characters', 
                                code='nomatch'
                            )],max_length=2, null=True, blank=True)
    zip_code            =   models.PositiveIntegerField(null=True, blank=True)
    ether_addr          =   models.CharField(
                            validators=[RegexValidator(
                                regex='^\w{42}$', 
                                message='Ether address length must be 42 characters', 
                                code='nomatch'
                            )], 
                            max_length=42, null=True, blank=True
                            )
    ether_part_amount   =   models.PositiveIntegerField(null=True, blank=True)
    telegram_addr       =   models.CharField(max_length=50, blank=True, null=True)

    bitcoin_balance     =   models.DecimalField(max_digits=11, decimal_places=4, default=0, 
                                validators=[MinValueValidator(Decimal('0.0000'))])
    ether_balance       =   models.DecimalField(max_digits=11, decimal_places=4, default=0, 
                                validators=[MinValueValidator(Decimal('0.0000'))])
    usd_balance         =   models.DecimalField(max_digits=11, decimal_places=2, default=0, 
                                validators=[MinValueValidator(Decimal('0.00'))])
    star_balance        =   models.DecimalField(max_digits=11, decimal_places=2, default=0, 
                                validators=[MinValueValidator(Decimal('0.00'))])
    bonus_star_balance  =   models.DecimalField(max_digits=11, decimal_places=2, default=0, 
                                validators=[MinValueValidator(Decimal('0.00'))])

    start_time          =   models.DateField(auto_now_add=True, editable=False)

    user_type           =   models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=NONE)

    email_verified      =   models.BooleanField(blank=True, default=False)
    phone_verified      =   models.BooleanField(blank=True, default=False)

    twitter_name        =   models.CharField(max_length=50, blank=True, null=True)
    facebook_url        =   models.URLField(blank=True, null=True)
    linkedin_url        =   models.URLField(blank=True, null=True)
    bitcoin_name        =   models.CharField(max_length=50, blank=True, null=True)
    reddit_name         =   models.CharField(max_length=50, blank=True, null=True)
    steemit_name        =   models.CharField(max_length=50, blank=True, null=True)

    referral_code       =   models.CharField(max_length=150, null=True, blank=True)
    referral_type       =   models.PositiveSmallIntegerField(choices=REFERRAL_CHOICES, default=NO_REFERRAL)
    referral_user       =   models.ForeignKey('self', on_delete=models.CASCADE, 
                                    related_name='referees', blank=True, null=True)

    whitepaper          =   models.BooleanField(default=False)
    token_sale          =   models.BooleanField(default=False)
    data_protection     =   models.BooleanField(default=False)

    @property
    def projects(self):
        return list(itertools.chain.from_iterable(
            [device.active_projects.all() for device in self.devices]))


    def __str__(self):
        return "%s %s" % (self.first_name or "", self.last_name or "")

    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return self.first_name if self.first_name else ""

    def set_referral_code(self, email):
        self.referral_code = "{0}_{1}".format(
            email.split('@')[0], "".join(random.choice(
            string.ascii_letters + string.digits) for i in range(10))
        )

    #######################################################################################
    # Contacting User
    
    def send_email(self, subject, message,
            from_email="no-reply@astraglobal.net"):
        """
        Sends an email to this user using the current STMP email
        middleware, with the subject and message inputed.
        """
        send_mail(
            subject = subject, 
            message = message, 
            from_email = from_email, 
            recipient_list = [self.email], 
            fail_silently = False
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
            from_email = "noreply@astraglobal.net", 
            recipient_list = [self.phone_number], 
            fail_silently = True
        )
        return True

    def validate_email(self):
        if self.email_verified:
            return False

        return self.send_email(
            "Activate Astra",
            ("{0},\n\n"
            "Welcome to Astra! Please click the following link to "
            "confirm your email address for Astra\n\n"
            "{1}\n\n"
            "After you do so, remember to fill out the rest of your ICO-"
            "KYC form to begin token sale.\n\n"
            "Best,\n\n"
            "The Astra Team ").format(
                self.first_name, 
                "{0}dashboard-login/?email-verify={1}".format(User.WEB_HEADER, self.email)
            ) 
        )

    def remind_validate_email(self):
        if self.email_verified:
            return False

        return self.send_email(
            "Reminder to Activate Astra",
            ("{0},\n\n"
            "Hi! We're emailing you again to remind you to "
            "confirm your email address for Astra\n\n"
            "{1}\n\n"
            "After you do so, remember to fill out the rest of your ICO-"
            "KYC form to begin token sale.\n\n"
            "Best,\n\n"
            "The Astra Team ").format(
                self.first_name, 
                "{0}dashboard-login/?email-verify={1}".format(User.WEB_HEADER, self.email)
            ) 
        )

    def reset_password_email(self):
        return self.send_email(
            "Reset Password",
            ("{0},\n\n"
            "Hi! Please click the following link to reset your password\n\n"
            "{1}/dashboard-change-password/?email={2}\n\n"
            "If you believe you have gotten this email in error, please ignore this message.\n\n"
            "Best,\n\n"
            "The Astra Team ").format(
                self.first_name, 
                User.WEB_HEADER,
                self.email,
            ) 
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

        self.add_promo_star_tokens(10)

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
    def add_promo_star_tokens(user, amount):
        user.star_balance += amount
        user.bonus_star_balance += amount
        if user.star_balance < 0:
            user.star_balance = 0
        if user.bonus_star_balance < 0:
            user.bonus_star_balance = 0
        user.save()    

    @staticmethod
    def add_star_tokens(user, amount):
        user.token_auth()
        user.star_balance += amount
        if user.star_balance < 0:
            amount = amo
            user.star_balance = 0
        user.save()

    @staticmethod
    def add_usd(user, amount):  
        user.token_auth()
        user.usd_balance += amount
        if user.usd_balance < 0:
            user.usd_balance = 0
        user.save()

    @staticmethod
    def add_bitcoin(user, amount):
        user.token_auth()
        user.bitcoin_balance += amount
        if user.bitcoin_balance < 0:
            user.bitcoin_balance = 0
        user.save()

    @staticmethod
    def add_ether(user, amount):
        user.token_auth()
        user.ether_balance += amount
        if user.ether_balance < 0:
            user.ether_balance = 0
        user.save()

    #######################################################################################
    # Passwords

    def change_password(self, old_password, new_password, confirm_new_password):
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

    def reset_password(self, new_password, confirm_new_password):
        """
        Reset's user password to new_password. Only to be done after 
        email confirmation.
        """
        valid_regex = "^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$"
        if not (new_password and confirm_new_password):
            PasswordChangeError.missing_fields()
        if len(new_password) < 6:
            PasswordChangeError.password_too_short()
        if not re.match(valid_regex, new_password):
            PasswordChangeError.invalid_characters()
        if new_password != confirm_new_password:
            PasswordChangeError.unmatching_passwords()
        
        self.set_password(new_password) 
        self.save()

    #######################################################################################
    # Authentication

    def ico_complete(self):
        """
        Checks to see if user has submitted all ICO-KYC form 
        data.
        """
        selfie = id_file = False
        
        # if self.files.filter(filetype="SF").exists:
        #     selfie = self.files.filter(filetype="SF").latest('created').verified
        # if self.files.filter(filetype="ID").exists:
        #     id_file = self.files.filter(filetype="ID").latest('created').verified

        return all([
            self.first_name,
            self.last_name,
            self.street_addr1, 
            self.city, 
            self.state, 
            self.country,
            self.phone_number, 
            self.zip_code,
            selfie,
            id_file,
            self.ether_addr, 
            self.ether_part_amount,
            self.whitepaper,
            self.token_sale,
            self.data_protection,
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
        if not self.ico_complete():
            raise TokenICOKYCError.incomplete_ICO()

    def boolean_token_auth(self):
        """
        Boolean, non-error raising version of the previous function
        """
        return (
            self.email_verified and 
            self.is_active and 
            self.ico_complete()
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
        if not user or not user.check_password(password):
            raise AuthenticationError.invalid_credentials()
        if not user.is_active:
            raise AuthenticationError.inactive_account()
        return user

    @staticmethod
    def login(email, password):
        """ 
        Logs in a user by first authenticating them, or raises an authentication error.
        """
        user = User.authenticate(email, password)
        if user: user.logged_in = True
        return user

    def logout(self):
        """
        Logs a user out.
        """
        self.logged_in = False


    #######################################################################################
    # Transactions (PyEthApp Abstractions)

    def send_funds(self, value):
        tx = eth.transact(self.ether_addr, value=value)
        return eth.find_transaction(tx)
        

    #######################################################################################
    # Referrals
    
    def referral_count(self):
        """
        The number of referral codes given by the user.
        """
        return self.referees.count()
    
    def add_referral(self, referral_code):
        """
        Adds referral to the referree's account, checking to see if the 
        referrer exists and hasn't exceeded their max referrals.
        """
        if not referral_code: 
            return False
        
        try:
            referrer = User.objects.get(referral_code=referral_code)
            if referrer == self:
                raise ReferralError.self_referral()
        except User.DoesNotExist:
            raise ReferralError.referral_code_error()
        if referrer.referral_count() >= 10:
            raise ReferralError.referral_max_error()
        if self.referral_user:
            if self.referral_user != referrer:
                raise ReferralError.referral_set()
            return False
        if referrer.referral_user and referrer.referral_user == self:
            raise ReferralError.circular_referral()

        referrer.referees.add(self)
        self.save()
        referrer.save()

        return referrer

    
