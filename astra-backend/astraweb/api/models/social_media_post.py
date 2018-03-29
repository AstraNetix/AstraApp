import hashlib
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class SocialMediaPost(models.Model):

    #######################################################################################
    # Meta Options

    class Meta:
        app_label       =   "api"
        db_table        =   "api_social_media_post"

    STAR_BONUS          =   5  # Amount of bonus star coins per post

    FACEBOOK            =   'FB'
    TWITTER             =   'TW'
    TELEGRAM            =   'TE'
    LINKEDIN            =   'LN'
    BITCOIN_TALK        =   'BT'
    REDDIT              =   'RD'
    OTHER               =   'OR'

    PLATFORM_CHOICES    =   (
                                (FACEBOOK, 'Facebook'),
                                (TWITTER, 'Twitter'),
                                (TELEGRAM, 'Telegram'),
                                (LINKEDIN, 'Linkedin'),
                                (BITCOIN_TALK, 'Bitcoin Talk'),
                                (REDDIT, 'Reddit'),
                                (OTHER, 'Other'),
                            )

    #######################################################################################
    # Fields
    
    uid                 =   models.CharField(max_length=10, null=True, validators=[RegexValidator(
                                regex='^\w{10}$', 
                                message='UID must be 10 hex characters', 
                                code='nomatch'
                            )], unique=True)
    platform            =   models.CharField(max_length=2, choices=PLATFORM_CHOICES, default=OTHER)
    content             =   models.TextField()
    user                =   models.ForeignKey(User, blank=False, related_name="post", on_delete="CASCADE")
    date                =   models.DateTimeField()
    verified            =   models.BooleanField(default=False)

    def __str__(self):
        return self.uid

    def verify(self):
        self.verified = True
        User.add_star_tokens(self.user, self.STAR_BONUS)

    def hash_code(self):
        post_hash = hashlib.sha256()
        post_hash.update(str(self.platform).encode('utf-8'))
        post_hash.update(str(self.user.email).encode('utf-8'))
        post_hash.update(str(self.content).encode('utf-8'))
        post_hash.update(str(self.date).encode('utf-8'))
        return post_hash.hexdigest()[:-10]
