import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        created = False
        
        if not User.objects.filter(email="skale1@berkeley.edu").exists():
            created = True
            User.objects.create_superuser(email="skale1@berkeley.edu", password=os.environ["SOHAM_PASSWORD"])

        soham = User.objects.get(email='skale1@berkeley.edu')
        if not soham.is_api_user:
            soham.is_api_user = True
            soham.save()

        if not User.objects.filter(email="rajeshktrivedi@gmail.com").exists():
            created = True
            User.objects.create_superuser(email="rajeshktrivedi@gmail.com", password=os.environ["RAJESH_PASSWORD"])

        rajesh = User.objects.get(email='rajeshktrivedi@gmail.com')
        if not rajesh.is_api_user:
            rajesh.is_api_user = True
            rajesh.save()

        if not User.objects.filter(email="apimaster@gmail.com").exists():
            created = True
            User.objects.create_api_user(email="apimaster@gmail.com", password=os.environ["API_PASSWORD"])

        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created new super and api users'))
        else:
            self.stdout.write(self.style.SUCCESS('Superusers with these email already exist'))