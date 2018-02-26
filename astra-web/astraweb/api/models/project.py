from __future__ import unicode_literals
import re

from django.db import models

class Project(models.Model):
    url = models.CharField(max_length=300, null=True)

    name = models.CharField(max_length=50, null=True)
    organization = models.CharField(max_length=50, null=True)   