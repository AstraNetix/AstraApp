from __future__ import absolute_import, unicode_literals
from celery import shared_task
from api.models.usage import Usage

@shared_task
def update_coarse_data():
    for usage in Usage.objects.all():
        usage.add_coarse_data()