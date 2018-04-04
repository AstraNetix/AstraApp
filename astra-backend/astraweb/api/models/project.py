from __future__ import unicode_literals
import re

from django.db import models

platform_choices = {
    "WIN": "Microsoft Windows",
    "MAC": "Apple Mac OS X",
    "LIN": "Linux on Intel",
    "NVI": "Nvidia GPU",
    "AMD": "AMD GPU",
    "AND": "Android",
    "BSD": "FreeBSD",
    "LAR": "Linux on ARM",
    "INT": "Intel GPU",
    "BOX": "Virtual Box",
}

class SeparatedValuesField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ', ')
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token).join('\n')

    def get_prep_value(self, value):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([s for s in value])

    def value_to_string(self, obj):
        if isinstance(obj, str):
            return obj
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class PlatformField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ', ')
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return [value[i:i+3] for i in range(0, len(value), 3)]

    def get_prep_value(self, value):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return "".join([s for s in value if s in platform_choices])
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class Project(models.Model):   

    url                 =   models.CharField(max_length=300, null=True, unique=True)

    name                =   models.CharField(max_length=50, null=True)
    sponsors            =   SeparatedValuesField(null=True)
    description         =   models.TextField(null=True)

    area                =   models.CharField(max_length=50, null=True)

    platforms           =   PlatformField(max_length=40, null=True)

    def __str__(self):
        return self.name