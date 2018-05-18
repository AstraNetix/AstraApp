from django.db import models
from api.models.task import Task
from api.models.device import Device

class DeviceTask(models.Model):

    #######################################################################################
    # Meta Options

    DOWNLOADED          =   'DLD' 
    DOWNLOADING         =   'DLG'
    ABORTED             =   'ABT'
    SUSPENDED           =   'SSP' 
    READY_TO_REPORT     =   'RTR'
    READY_TO_START      =   'RTS'
    WAITING_TO_RUN      =   'WTR'
    RUNNING             =   'RNG'
    USER_SUSPENDED      =   'USP'
    UPLOADING           =   'UPL'
    CPU_BENCHMARKS      =   'CPU'
    PROJECT_SUSPENDED   =   'PRO'
    TIME_OF_DAY         =   'TOD'
    COMPLETED           =   'CMP'

    EXECUTING           =   'EXE'
    UNINITIALIZED       =   'UNI'

    STATE_OPTIONS       =   (
                                (DOWNLOADED,            'Downloaded'),
                                (DOWNLOADING,           'Downloading'),
                                (ABORTED,               'Aborted'),
                                (SUSPENDED,             'Suspended'),
                                (READY_TO_REPORT,       'Ready to Report'),
                                (READY_TO_START,        'Ready to Start'),
                                (WAITING_TO_RUN,        'Waiting to Run'),
                                (RUNNING,               'Running'),
                                (USER_SUSPENDED,        'User Suspended'),
                                (UPLOADING,             'Uploading'),
                                (CPU_BENCHMARKS,        'CPU Benchmarks taking place'),
                                (PROJECT_SUSPENDED,     'Project suspended'),
                                (TIME_OF_DAY,           'Suspended due to time of day'),
                                (COMPLETED,             'Completed'),
                            )

    ACTIVE_OPTIONS      =   (
                                (EXECUTING,             'Executing'),
                                (UNINITIALIZED,         'Uninitialized'),
                            ) 

    #######################################################################################
    # Fields

    task                =   models.ForeignKey(to=Task, related_name='device_tasks', on_delete=models.CASCADE)
    device              =   models.ForeignKey(to=Device, related_name='tasks_meta', on_delete=models.CASCADE)
    recieved            =   models.DateTimeField()
    state               =   models.CharField(max_length=50, choices=STATE_OPTIONS)
    active_state        =   models.CharField(max_length=50, choices=ACTIVE_OPTIONS)
    fraction_done       =   models.FloatField()
    cpu_time_running    =   models.FloatField()
    cpu_time_remaining  =   models.FloatField()
    completed           =   models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def complete(self):
        self.state = self.COMPLETED
        self.completed = True
        self.save()
