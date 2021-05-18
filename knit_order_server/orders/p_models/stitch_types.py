from django.db import models
import re
from .image_model import KImage

class StitchTypeModel(models.Model):
    stitch_type= models.CharField(null=True, max_length=30,  blank=True, default=None)
    code= models.CharField(null=True, max_length=30,  blank=True, default=None)
    description = models.CharField(null=True, max_length=100,  blank=True, default=None)
    images = models.ManyToManyField(KImage, blank=True, default=None)

    class Meta:
        db_table = 'stitch_type'
        verbose_name = 'Stitch Type'
    
    def save(self, *args, **kwargs):
        if not self.stitch_type:
            raise ValueError("Please enter stitch type")
        else:
            replaced_txt = re.sub(r'\W+', '-', self.stitch_type)
            self.code = replaced_txt.upper()

        super().save(*args, **kwargs)


    def __str__(self):
        return self.code
