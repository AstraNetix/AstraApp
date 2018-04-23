import os
import django

from django.core.management.base import BaseCommand, CommandError

from api.models.email import Email
from api.models.user import User

emails = [
    {
        'name': 'Email Verification',
        'from_email': 'no-reply@astraglobal.net',
        'subject': 'Activate Astra',
        'header': 'Hi {{first_name}},',
        'content': ("Welcome to Astra! Please click the following link to "
            "confirm your email address for Astra\n\n"
            "{}dashboard-login/?email-verify={{{email}}}\n\n"
            "After you do so, remember to fill out the rest of your ICO-"
            "KYC form to begin token sale.").format(User.WEB_HEADER),
        'footer': "Best,\n\nThe Astra Team ",
    },
     {
        'name': 'Reset Password',
        'from_email': 'no-reply@astraglobal.net',
        'subject': 'Reset your password',
        'header': 'Hi {{first_name}},',
        'content': ("Please click the following link to reset your password\n\n"
            "{}/dashboard-change-password/?email={{{email}}}\n\n"
            "If you believe you have gotten this email in error, please ignore 
            "this message.").format(User.WEB_HEADER),
        'footer': "Best,\n\nThe Astra Team ",
    },
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        for email in emails:
            if not Email.objects.filter(subject=email['subject']).exists():
                email = Email(**email)
                email.save()
        self.stdout.write(self.style.SUCCESS('Successfully created all emails.'))