import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "astraweb.settings")
django.setup()

from api.models.user import User
from api.models.email import Email

user = User.objects.get(email='skale1@berkeley.edu')
email = Email.objects.all()[0]

email.send(user)