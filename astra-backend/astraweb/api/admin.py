from django.contrib import admin

from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from api.models.user import User
from api.models.device import Device
from api.models.project import Project

class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = (
            'email', 
            'password', 
            'first_name', 
            'middle_name',
            'last_name', 
            'phone_number', 
            'street_addr1',  
            'street_addr2', 
            'city', 
            'state',  
            'country', 
            'zip_code', 
            'id_file', 
            'selfie', 
            'ether_addr', 
            'telegram_addr',
            'ether_part_amount', 
            'email_verified', 
            'phone_verified', 
            'user_type',
            'twitter_name',
            'facebook_url',
            'linkedin_url',
            'bitcoin_name',
            'reddit_name',
            'steemit_name',
            'referral',
        )



admin.site.register(User)
admin.site.register(Device)
admin.site.register(Project)



