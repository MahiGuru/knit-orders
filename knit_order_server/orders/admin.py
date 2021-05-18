from django.contrib import admin
from .p_models.image_model import KImage
from .p_models.measurments_model import MeasurementModel
from .p_models.order_model import Orders
from .p_models.sizes_model import SizeModel
from .p_models.stitch_types import StitchTypeModel


# Register your models here.
admin.site.register(KImage)
admin.site.register(MeasurementModel)
admin.site.register(Orders)
admin.site.register(SizeModel)
admin.site.register(StitchTypeModel)