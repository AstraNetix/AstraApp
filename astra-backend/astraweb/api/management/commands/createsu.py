from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        created = False
        
        if not User.objects.filter(email="skale1@berkeley.edu").exists():
            created = True
            User.objects.create_superuser(email="skale1@berkeley.edu", password="Starry1@nighT")
        if not User.objects.filter(email="rajeshktrivedi@gmail.com").exists():
            created = True
            User.objects.create_superuser(email="rajeshktrivedi@gmail.com", password="Astra987")
            
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created new super users'))
        else:
            self.stdout.write(self.style.SUCCESS('Superusers with these email already exist'))