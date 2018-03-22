import time
import hashlib

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator

from django.contrib.auth import get_user_model
from api.models.project import Project

from api.exceptions.device_exceptions import QuitProjectError, StartProjectError, DeviceClientError
from api.exceptions.user_exceptions import AuthenticationError

from api.pubnub_client import PubNubClient

User = get_user_model()

class Device(models.Model):

    #######################################################################################
    # Meta Options

    class Meta:
        app_label       =   "api"
        db_table        =   "api_device"

    def hashCode(self):
        code = hashlib.sha1()
        code.update(self.name.encode('utf-8'))
        code.update(self.company.encode('utf-8'))
        code.update(self.model.encode('utf-8'))
        code.update(self.user.email.encode('utf-8'))
        return code.hexdigest()

    @classmethod
    def setup_client(cls):
        cls.pubnub = PubNubClient(cls)

    @classmethod
    def quit(cls):
        cls.pubnub.quit_client()

    def __str__(self):
        return self.name


    #######################################################################################
    # Fields

    uid                 =   models.CharField(
                            validators=[RegexValidator(
                                regex='^\w{40}$', 
                                message='UID length (from SHA1) must be 40 characters', 
                                code='nomatch'
                            )], max_length=40, default="", blank=True)

    name                =   models.CharField(max_length=45, null=True, blank=True)
    company             =   models.CharField(max_length=45)
    model               =   models.CharField(max_length=30)

    run_on_batteries    =   models.BooleanField(default=False, blank=True)
    run_if_active       =   models.BooleanField(default=False, blank=True)
    start_hour          =   models.SmallIntegerField(default=0, blank=True, validators=[
                                MaxValueValidator(23), MinValueValidator(0)])
    end_hour            =   models.SmallIntegerField(default=23, blank=True, validators=[
                                MaxValueValidator(23), MinValueValidator(0)])
    max_CPUs            =   models.SmallIntegerField(default=2, blank=True, validators=[
                                MaxValueValidator(8), MinValueValidator(0)])
    disk_max_percent    =   models.SmallIntegerField(default=50, blank=True, validators=[
                                MaxValueValidator(0), MinValueValidator(100)])
    ram_max_percent     =   models.SmallIntegerField(default=50, blank=True, validators=[
                                MaxValueValidator(0), MinValueValidator(100)])
    cpu_max_percent     =   models.SmallIntegerField(default=50, blank=True, validators=[
                                MaxValueValidator(0), MinValueValidator(100)])

    active_projects     =   models.ManyToManyField(Project, blank=True, related_name="active_projects")
    dormant_projects    =   models.ManyToManyField(Project, blank=True, related_name="dormant_projects")
    past_projects       =   models.ManyToManyField(Project, blank=True, related_name="past_projects")

    user                =   models.ForeignKey(User, blank=True, related_name="device", on_delete="CASCADE")

    active              =   models.BooleanField(default=False, blank=True)


    ##############################################################################################
    # Management

    @classmethod
    def create(cls, kwargs):
        try:
            user = User.objects.get(email=kwargs.pop('email'))
            device = cls(**kwargs)
            device.user = user

            if not device.name:
                device.name = "{0}'s {1} {2}".format(
                    device.user.first_name, 
                    device.company, 
                    device.model,
                )
            device.uid = device.hashCode()
            device.save()
            print("creating device...")
            return device
        except User.DoesNotExist:
            # Handle UserDoesNotExist 
            pass

    def quit_boinc(self):
        Device.pubnub.publish(message={
            "function": "quit"
        }, device_id=self.uid)

    
    ##############################################################################################
    # Projects 

    def start_project(self, pk):
        project = Project.objects.get(pk=pk)
        if not project:
            raise StartProjectError.project_nonexistent()

        time_token = PubNubClient.publish(self.uid, {
            "function": "start-project",
            "url": project.url
        })  

        if not Device.pubnub.check_for_response():
            raise DeviceClientError.device_unreachable()

    def quit_project(self, pk):
        project = Project.objects.get(pk=pk)
        if not project:
            raise QuitProjectError.project_nonexistent()

        time_token = Device.pubnub.publish(self.uid, {
            "function": "quit-project",
            "url": project.url
        }) 
                
        if not Device.pubnub.check_for_response():
            raise DeviceClientError.device_unreachable()

    def start_project_async(self, url):
        project = self.active_projects.get(url=url)
        finished_project = self.past_projects.get(url=url)
        
        if not project:
            raise StartProjectError.project_active()
        if finished_project:
            raise StartProjectError.project_finished()

        self.active_projects.add(project)
        self.dormant_projects.remove(project)

    def quit_project_async(self, url):
        project = self.active_projects.get(url=url)
        finished_project = self.past_projects.get(url=url)

        if not project:
            raise QuitProjectError.project_not_active()
        if finished_project:
            raise QuitProjectError.project_finished()

        self.active_projects.remove(project)
        self.dormant_projects.add(project)

    def project_status(self):
        Device.pubnub.publish(message={
            "function": "project-status",
        }, device_id=self.uid)

        if not Device.pubnub.check_for_response():
            raise DeviceClientError.device_unreachable()
