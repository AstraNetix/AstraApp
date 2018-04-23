import re

from django.db import models
from django.core.mail import send_mail, send_mass_mail, get_connection
from django.core.mail.message import EmailMessage

from api.models.file import File
from api.models.user import User

class Email(models.Model):
    """
    A model to store often used email templates. Fields in the header, content, 
    and footer fields of the form {{field}} are replaced with their corresponding
    user fields.
    """
    name            =   models.CharField(max_length=200, null=True)
    from_email      =   models.EmailField()
    reply_to        =   models.EmailField(null=True, blank=True)
    subject         =   models.EmailField()
    header          =   models.TextField(null=True, blank=True)
    content         =   models.TextField()
    footer          =   models.TextField(null=True, blank=True)
    attachments     =   models.ManyToManyField(File, related_name='emails')
    times_sent      =   models.SmallIntegerField(default=0) 

    def send(self, to, bcc=None, cc=None):
        """
        Sends this email to the list of the users in TO, with additional    
        BCC and CC arguments. 
        """
        to = [to] if isinstance(to, User) else to
        bcc = [bcc] if isinstance(to, User) else bcc
        cc = [cc] if isinstance(to, User) else cc

        connection = get_connection()

        for user in to:
            email = EmailMessage(
                subject     =   self.subject, 
                body        =   self._parse_text(self.content, user),
                from_email  =   self.from_email,
                to          =   user.email,
                bcc         =   [user.email for user in bcc],
                connection  =   connection,
                cc          =   [user.email for user in cc],
                reply_to    =   self.reply_to
            )
            for attachment in self.attachments:
                email.attach(attachment.name, attachment.datafile, attachment.mimetype)

            email.send()
            self.times_sent += 1

        self.save()

    def _parse_text(self, text, user):
        return_text = ''
        for i in range(len(text)):
            if text[i] == '{' and text[i+1] == '{':
                i = j = i + 2
                while text[j] != '}' and text[j+1] != '}':
                    j += 1
                return_text += getattr(user, text[i:j])
                i = j + 2
            else:
                return_text += text[i]
        return return_text