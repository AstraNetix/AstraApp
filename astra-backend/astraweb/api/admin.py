from django import forms
from django.contrib import admin

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import FieldListFilter

from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model

from api.models.device import Device
from api.models.project import Project
from api.models.social_media_post import SocialMediaPost

User = get_user_model()

class UserCreationForm(BaseUserCreationForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    name                =   forms.CharField(label='Name') 
    password            =   forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password    =   forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        try:
            user.first_name, user.last_name = self.cleaned_data["name"].split(" ")
        except ValueError:  # If for some reason, user only gave first name
            user.first_name = self.cleaned_data["name"]

        if commit:
            user.save()
        return user

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
            'referral_code',
            'referral_type',
            'referral_user',
        )


class UserChangeForm(BaseUserChangeForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ('logged_in', 'is_active', 'email_verified', 'phone_verified', 'bitcoin_balance', 
                'ether_balance', 'usd_balance', 'star_balance', 'bonus_star_balance', 'referral_code',
                'whitepaper', 'token_sale', 'data_protection')

    list_display = ('name', 'email', 'is_superuser', 'user_type')
    list_filter = ('is_superuser', 'user_type', 'email_verified')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'user_type')}),
        ('Status', {'fields': ('logged_in', 'is_active', 'is_staff', 'is_superuser', 'is_api_user')}),
        ('Personal info', {'fields': ('first_name', 'middle_name', 'last_name', 'phone_number', 'ether_addr')}),
        ('Location', {'fields': ('street_addr1', 'street_addr2', 'city', 'state', 'country', 'zip_code')}),
        ('Files', {'fields': ('id_file', 'selfie')}),
        ('Social Media', {'fields': ('telegram_addr', 'twitter_name', 'facebook_url', 'linkedin_url', 'bitcoin_name', 'reddit_name', 'steemit_name')}),
        ('Balance', {'fields': ('bitcoin_balance', 'ether_balance', 'usd_balance', 'star_balance', 'bonus_star_balance')}),
        ('Verifications', {'fields': ('email_verified', 'phone_verified', 'whitepaper', 'token_sale', 'data_protection')}),
        ('Referrals', {'fields': ('referral_code', 'referral_type', 'referral_user')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password', 'confirm_password')}
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)

    def name(self, obj):
        return "%s %s" % (obj.first_name or "", obj.last_name or "")


class SocialMediaPostAdmin(admin.ModelAdmin):
    search_fields = ('user', 'date')
    ordering = ('date',)

    list_display = ('uid', 'user', 'date', 'verified', 'platform')
    list_filter = ('verified', 'platform')

    readonly_fields = ('uid', 'date', 'user', 'platform', 'content')
    fields = (('uid', 'verified'), 'platform', 'content', 'user', 'date')


# class PlatformFilter(FieldListFilter):
#     title = _('Platform')

#     parameter_name = 'platforms'

#     def lookups(self, request, model_admin):
#         return(
#             ("WIN", _("Microsoft Windows")),
#             ("MAC", _("Apple Mac OS X")),
#             ("LIN", _("Linux on Intel")),
#             ("NVI", _("Nvidia GPU")),
#             ("AMD", _("AMD GPU")),
#             ("AND", _("Android")),
#             ("BSD", _("FreeBSD")),
#             ("LAR", _("Linux on ARM")),
#             ("INT", _("Intel GPU")),
#             ("BOX", _("Virtual Box")),
#         )
    
#     def queryset(self, request, queryset):
#         return_query = Project.objects.none()
#         for project in queryset:
#             if self.value() in PlatformField.to_python(project.platforms):
                    



class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('area', 'platforms')

    list_display = ('name', 'base_url', 'sponsors', 'area')
    list_filter = ('area', 'platforms')

    readonly_fields = ('base_url', 'name', 'sponsors', 'area', 'platforms')
    fields = ('name', 'base_url', 'area', 'description', 'sponsors', 'platforms')

    def base_url(self, obj):
        return format_html('<a href="%s">%s</a>' % (obj.url, obj.url))
    

admin.site.register(User,               UserAdmin               )
admin.site.register(SocialMediaPost,    SocialMediaPostAdmin    )
admin.site.register(Device                                      )
admin.site.register(Project,            ProjectAdmin            )



