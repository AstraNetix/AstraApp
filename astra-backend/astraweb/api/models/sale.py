from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Sale(models.Model):

    #######################################################################################
    # Meta Options

    class Meta:
        app_label       =   "api"
        db_table        =   "api_sale"


    #######################################################################################
    # Fields
    
    name                =   models.CharField(max_length=100, null=True, blank=True)

    duration            =   models.DurationField()
    actionable          =   models.BooleanField(default=False)  
    markdown            =   models.SmallIntegerField(default=0, blank=True, validators=[
                                MaxValueValidator(0), MinValueValidator(100)])

