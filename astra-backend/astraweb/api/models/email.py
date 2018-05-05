import re 
from django.db import models
from django.core.mail import send_mail, send_mass_mail, get_connection
from mail_templated import EmailMessage

from api.models.file import File
from api.models.user import User
from api.exceptions.email_exceptions import ParsingError

class Email(models.Model):
    """
    A model to store often used email templates. To add user information into the 
    templates, use the format {{field}} for a field on the user to replace it.

    To traverse database relationships, use a Pipe "|" to reference fields on a 
    related model, such as with {{referral_user|email}}. This works with One-to-
    One or ForeignKey relationships.

    For ManytoMany relationships or reverse ForeignKeys, use the same format as 
    above, except the rest of the query will be executed on each object in the
    relationship set, separated by a ", ". For example, {{devices|uid}} will 
    give "1ae39, a390c3, 99b3e2".

    Pipes can traverse relationship chains of any length, for example, 
    {{user|projects|device_set|user|referees|email}}
    """

    FROM_CHOICES    =   (
                            ('no-reply@astraglobal.net', 'No Reply'),
                            ('support@astraglobal.net', 'Support'),
                            ('billing@astraglobal.net', 'Billing'),
                            ('info@astraglobal.net', 'Info'),
                            ('rajesh@astraglobal.net', 'Rajesh'),
                            ('team@astraglobal.net', 'Team'),
                            ('feedback@astraglobal.net', 'Feedback'),
                            ('soham@astraglobal.net', 'Soham'),
                        )

    name            =   models.CharField(max_length=200, null=True)
    from_email      =   models.EmailField(choices=FROM_CHOICES)
    reply_to        =   models.EmailField(null=True, blank=True)
    subject         =   models.CharField(max_length=200)
    content         =   models.TextField()
    attachments     =   models.ManyToManyField(File, related_name='emails', blank=True)
    times_sent      =   models.SmallIntegerField(default=0) 

    def send(self, to):
        """
        Sends this email to the list of the users in TO, with additional    
        BCC and CC arguments. 
        """
        to = [to] if isinstance(to, User) else to
        connection = get_connection()

        for user in to:
            email = EmailMessage(
                template_name   =   'api/email.html',
                context         =   {'subject': Email._parse_text(self.subject, user),
                                    'content': Email._parse_text(self.content, user),
                                    'footer': Email._parse_text(self.footer, user)},
                from_email      =   self.from_email,
                to              =   [user.email],
                connection      =   connection,
                reply_to        =   self.reply_to
            )
            for attachment in self.attachments.all():
                email.attach(attachment.name, attachment.datafile, attachment.mimetype)

            email.send()
            self.times_sent += 1

        self.save()

    def mass_send(self):
        self.send(to=User.objects.all())

    @staticmethod
    def _parse_text(text, user):
        def traverse_path(model, path):
            try:
                name = next(path)
                try:
                    field = getattr(model, name)
                except AttributeError:
                    raise ParsingError.field_does_not_exist(model, name)
            except StopIteration:
                return "" 

            # Is a foreign key or one-to-one field
            if isinstance(field, models.Model): 
                return traverse_path(field, path)
            # Is a many-to-many relation or a reverse foreign key
            elif type(model)._meta.get_field(name).__class__.__name__ in ('ManyToOneRel', 'ManyToManyField'): 
                return ", ".join([traverse_path(obj, path) for obj in field.all()])
            return str(field)

        pattern = re.compile(r"\<\/[a-zA-Z][a-zA-Z0-9_|]*\/\>")
        for match in re.finditer(pattern, text):
            text = text.replace(match.group(), traverse_path(user, iter(match.group()[2:-2].split('|'))))
        return text
        
