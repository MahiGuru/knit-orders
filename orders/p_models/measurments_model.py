from django.db import models
import re

class MeasurementModel(models.Model):
    unit= models.CharField(null=True, max_length=30,  blank=True, default=None) 
    blouse_opening= models.CharField(null=True, max_length=30,  blank=True, default=None) 
    blouse_length= models.IntegerField()
    arm_hole_length= models.IntegerField()
    lower_bust_length= models.IntegerField()
    bust_length= models.IntegerField()
    shoulder_length= models.IntegerField()
    neck_front_length= models.IntegerField()
    neck_back_length= models.IntegerField()
    sleeve_length= models.IntegerField() 
    sleeve_width_length= models.IntegerField()


    class Meta:
        db_table = 'measurements'
        verbose_name = 'Measurement'
    
    def save(self, *args, **kwargs):
        if not self.size:
            raise ValueError("Please enter Measurement")
        else:
            replaced_txt = re.sub(r'\W+', '-', self.size)
            self.code = replaced_txt.upper()

        super().save(*args, **kwargs)


    def __str__(self):
        return self.code
