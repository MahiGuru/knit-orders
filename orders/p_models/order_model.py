from django.db import models

from datetime import datetime
from django.utils.timezone import now

from .image_model import KImage
from .timestamp_model import TimestampedModel 
from .sizes_model import SizeModel
from .measurments_model import MeasurementModel

class Orders(TimestampedModel):

    # Order basic info
    stitch_type = models.CharField(null=True, max_length=80,  default=None) 
    isClothAvailable = models.BooleanField(default=False, blank=True, null=True)
    isStitchType = models.IntegerField(blank=False, null=False, default=0)
    expected_date = models.DateField(auto_now=False) 
    extra_notes = models.CharField(default=None, max_length=180, blank=True, null=True)

    # Order details
    images = models.ManyToManyField(KImage, blank=True, default=None)
    clothSize = models.ManyToManyField(SizeModel, blank=True, null=True)
    measurements = models.ForeignKey(MeasurementModel, on_delete=models.CASCADE, blank=True, null=True)
    
    #Order belongs to vendor
    user = models.IntegerField(blank=True, null=True) 

    class Meta:
        db_table = 'orders'
        managed = True
    
    def __str__(self):
        return self.stitch_type

