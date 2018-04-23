import os
import sys
import django
from django.conf import settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "astraweb.settings")

    # settings.configure(DEBUG=True)
    # django.setup()
    # if '--pn' in sys.argv:
    #     sys.argv.remove('--pn')

    #     from api.models.device import Device
    #     Device.setup_client()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)