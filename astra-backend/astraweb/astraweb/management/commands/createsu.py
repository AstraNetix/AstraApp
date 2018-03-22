from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class SuperUserCreationCommand(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "skale1@berkeley.edu", "Starry1@nighT")
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))