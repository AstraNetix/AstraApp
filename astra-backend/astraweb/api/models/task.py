from django.db import models
from api.models.project import Project
from api.models.device import Device

class Task(models.Model):
    name                =   models.CharField(max_length=500, primary_key=True)
    devices             =   models.ManyToManyField(to=Device, related_name='tasks', 
                                through='DeviceTask')
    project             =   models.ForeignKey(to=Project, related_name='task', 
                                on_delete=models.CASCADE)
    due                 =   models.DateTimeField()
    app_version         =   models.SmallIntegerField()