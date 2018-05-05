from django import forms
from django.contrib import admin

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import FieldListFilter

from django.utils.html import format_html
from django.urls import reverse, path
from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse

from django.contrib.auth import get_user_model

from api.models.device import Device
from api.models.project import Project
from api.models.social_media_post import SocialMediaPost
from api.models.file import File
from api.models.email import Email
from api.exceptions.email_exceptions import ParsingError

User = get_user_model()

class SendEmailForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.email = kwargs.pop('email', None)
        super().__init__(args, kwargs)
        self.fields['from_email'].widget = forms.ChoiceField(
            choices=Email.FROM_CHOICES, 
            default=self.email.from_email
            )

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    from_email = forms.ChoiceField(choices=Email.FROM_CHOICES)
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    def send_email(self):
        self.email.from_email = self.cleaned_data['from_email']
        self.email.send(to=self.cleaned_data['users'])
        self.email.save()

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
                'whitepaper', 'token_sale', 'data_protection', 'ether_part_amount', 'referral_user')

    list_display = ('name', 'email', 'is_superuser', 'user_type')
    list_filter = ('is_superuser', 'user_type', 'email_verified')
    actions = ['send_validation_email', 'send_email']

    fieldsets = (
        (None, {'fields': ('email', 'password', 'user_type')}),
        ('Status', {'fields': ('logged_in', 'is_active', 'is_staff', 'is_superuser', 'is_api_user')}),
        ('Personal info', {'fields': ('first_name', 'middle_name', 'last_name', 'phone_number', 'ether_addr')}),
        ('Location', {'fields': ('street_addr1', 'street_addr2', 'city', 'state', 'country', 'zip_code')}),
        ('Social Media', {'fields': ('telegram_addr', 'twitter_name', 'facebook_url', 'linkedin_url', 'bitcoin_name', 'reddit_name', 'steemit_name')}),
        ('Ether Contribution', {'fields': ('ether_part_amount',)}),
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
                
    def send_validation_email(self, request, queryset):
        for user in queryset:
            user.validate_email()
        self.message_user(request, "Email verification emails successfully sent.")

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

class FileAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    ordering = ('created',)

    list_display = ('name', 'filetype', 'user', 'created')
    list_filter = ('filetype', 'verified')

    readonly_fields = ('created', 'name', 'user', 'datafile', 'filetype')
    fields = (('name', 'verified'), 'datafile', 'user', 'created')

class EmailAdmin(admin.ModelAdmin):
    search_fields = ('name',)

    list_display = ('name', 'from_email', 'times_sent', 'email_actions')
    list_filter = ('from_email',)

    readonly_fields = ('times_sent', 'email_actions')
    fields = ('name', 'from_email', 'reply_to', 'subject','content', 'attachments', 'times_sent')

    def get_urls(self):
        custom_urls = [
            path(
                r'^(?P<account_id>.+)/send/$',
                self.admin_site.admin_view(self.send_email),
                name='Send Email'
            ),
        ]
        return super().get_urls() + custom_urls

    def email_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Send</a>',
            reverse('admin:email-send', args=[obj.pk]),
        )
    
    email_actions.short_description = 'Actions'
    email_actions.allow_tags = True

    def send_email(self, request, email_id):
        email = self.get_object(request, email_id)
        if request.method != 'POST':
            form = SendEmailForm(email=email)
        else:
            form = SendEmailForm(request.POST, email=email)
            if form.is_valid():
                try:
                    form.send_email()
                except ParsingError as pe:
                    pass
                else:
                    self.message_user("Email successfully sent to {} user{}".format(
                        len(users), 's' if len(users) < 2 else ''))
                    url = reverse(
                        'admin:email_email_change',
                        args=[email.pk],
                        current_app=self.admin_site.name,
                    )
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['email_form'] = form
        context['subject'] = email.subject
        context['content'] = email.content
        return TemplateResponse(
            request, 
            'admin/send_email.html',
            context
        )


admin.site.register(User,               UserAdmin               )
admin.site.register(SocialMediaPost,    SocialMediaPostAdmin    )
admin.site.register(Device                                      )
admin.site.register(Project,            ProjectAdmin            )
admin.site.register(File,               FileAdmin               )
admin.site.register(Email,              EmailAdmin               )


