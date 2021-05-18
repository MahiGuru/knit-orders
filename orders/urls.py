from django.urls import path
from .p_views.stitchtype_view import StitchTypeViewSet
from .p_views.measurements_view import MeasurementsViewSet
from .p_views.image_view import ImageViewSet
from .p_views.order_view import OrdersViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stitch-type', StitchTypeViewSet, basename='stitchtype')
router.register(r'measurements', MeasurementsViewSet, basename='measurements')
router.register(r'images', ImageViewSet)
router.register(r'orders', OrdersViewSet) 

urlpatterns =  router.urls
