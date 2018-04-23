from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from api.models.usage import Usage

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astraweb.settings')

app = Celery('api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        update_coarse_data.s(),
    )

@app.task(bind=True)
def update_coarse_data():
    for usage in Usage.objects.all():
        usage.add_coarse_data()