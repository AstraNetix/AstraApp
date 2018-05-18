from django.db import models
from django.core.validators import RegexValidator
from api.exceptions.usage_exceptions import DataException

# Holds data for past 24 hours, 1 point for every 5 min, each point 3 digits in length
fine_regex      =   RegexValidator(
                        regex='^[0-9]{864}$', 
                        message='CPU usage string must be 864 numerical characters', 
                        code='nomatch'
                    )
fine_default    =   "".join('000' for i in range(864))

# Holds data for the past 90 days, 1 point for every day, each point 3 digits in length
coarse_regex    =   RegexValidator(
                        regex='^[0-9]{240}$', 
                        message='CPU usage string must be 240 numerical characters', 
                        code='nomatch'
                    )
coarse_default  =   "".join('000' for i in range(240))

class DataField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return [int(value[i:i+3]) for i in range(0, len(value), 3)]

    def get_prep_value(self, value):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return "".join([s for s in value])
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class Data(models.Model):

    cpu_fine        =   DataField(validators=[fine_regex], max_length=864, default=fine_default)    
    gpu_fine        =   DataField(validators=[fine_regex], max_length=864, default=fine_default)
    disk_fine       =   DataField(validators=[fine_regex], max_length=864, default=fine_default)
    network_fine    =   DataField(validators=[fine_regex], max_length=864, default=fine_default)  

    cpu_course      =   DataField(validators=[coarse_regex], max_length=144, default=coarse_default)    
    gpu_course      =   DataField(validators=[coarse_regex], max_length=144, default=coarse_default)
    disk_course     =   DataField(validators=[coarse_regex], max_length=144, default=coarse_default)
    network_course  =   DataField(validators=[coarse_regex], max_length=144, default=coarse_default) 

    def add_data(self, data_type, data):
        if data_type in ['cpu_course', 'gpu_course', 'disk_course', 'network_course']:
            raise DataException.adding_coarse()

        setattr(self, data_type, [data] + getattr(self, data_type)[1:])
        self.save()

    def add_coarse_data(self):
        for data_type in ['cpu', 'gpu', 'disk', 'network']:
            data_type = '{}_coarse'.format(data_type)
            old_data = getattr(self, data_type)[1:]
            setattr(self, data_type, [getattr(self, '{}_fine'.format(data_type))]+ old_data)