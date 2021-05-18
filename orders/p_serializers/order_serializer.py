from rest_framework import serializers

from ..p_models.image_model import KImage 
from ..p_models.order_model import Orders 
from ..p_models.sizes_model import SizeModel


from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from .image_serializer import ImageSerializer
from .size_serializers import SizeSerializer 

import re

import logging
logger = logging.getLogger(__name__)
 
class OrderSerializer(serializers.ModelSerializer):

    cloth_size = serializers.SerializerMethodField(read_only=True)
    measurements = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    errors = {}


    def get_measurements(self,obj):
        serializer = CategorySerializer(obj.category, many=True)
        return serializer.data 

    def get_cloth_size(self,obj):
        serializer = SubCategorySerializer(obj.sub_category, many=True)
        return serializer.data

    def get_images(self, obj):
        serializer = ImageSerializer(obj.images, many=True)
        return serializer.data 

        
    class Meta:
        model = Orders
        fields = ('id', 'stitch_type','isClothAvailable', 'isStitchType', 'expected_date', 'extra_notes', 'images', 'measurements', 'cloth_size')

    def validate(self, data):
        self.errors = {}
        data = self.initial_data.get('order')
        if self.instance is None:
            if data.get('stitch_type') is None:
                logger.error("Stitch type is required")
                raise serializers.ValidationError("Stitch type is required")
             
            if self.instance is None and data.get('expected_date'):
                data['expected_date'] = data.get('expected_date', None)
            else:
                logger.error("Expected date is required")
                self.errors['expected_date_required'] = "Expected date is required"
            if self.instance is None and data.get('user'):
                data['user'] = data.get('user', None)
            else:
                logger.error("Order User is required")
                self.errors['user_required'] = "Order user is required"
            logger.error(self.errors)
            raise serializers.ValidationError(self.errors)
        return data

    def create(self, validated_data):
        #Handling many to many fields
        validated_data = self.initial_data.get("order")
        orders_relations = self.initial_data.get("orders_relations")
        
        order = Orders.objects.create(**validated_data) 
        self.setOrderRelations(order, orders_relations)
        
        product.save() 
        return product

    def update(self, instance, validated_data):
        order_data = self.initial_data.get("order")
        orders_relations = self.initial_data.get("orders_relations")
        
        instance.title = order_data.get('title', instance.title)
        instance.description = order_data.get('description', instance.description)
        instance.quantity = order_data.get('quantity', instance.quantity)
        instance.price = order_data.get('price', instance.price)
        instance.user = order_data.get('user', instance.user)
        instance.in_stock = order_data.get('in_stock', instance.in_stock)

        self.setOrderRelations(instance, orders_relations)
        instance.save() 
        return instance

    def setOrderRelations(self, order, orders_relations):
        # COLORS RELATION HERE
        if order:
            if orders_relations.get('sizes'):
                if isinstance(orders_relations.get('sizes'), list):
                    size = list(SizeModel.objects.filter(id__in=orders_relations.get('sizes')))
                    product.sizes.set(size)
                
                elif isinstance(orders_relations.get('sizes'), str):
                    size_arr = orders_relations.get('sizes').split(",")
                    size = list(SizeModel.objects.filter(id__in=size_arr))
                    product.sizes.set(size)
                else:
                    logger.warning("NOT SAVED SIZES : Expected color ids should be an array bug got a {} ".format(type(sizes)))
            
            # IMAGES RELATION HERE
            if self.initial_data.get('images'):
                for e in product.images.all():
                    instance.images.remove(e)
                    KImage.objects.get(id=e.id).delete()
                for image in self.initial_data.get('images'):
                    c_image= self.initial_data.get('images')[image]
                    images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='products/product_'+str(product.id), size=c_image.size)
                    product.images.add(images)
            
            # IMAGES RELATION HERE
            if self.initial_data.get('measurements'):
                for e in product.images.all():
                    instance.images.remove(e)
                    KImage.objects.get(id=e.id).delete()
                for image in self.initial_data.get('images'):
                    c_image= self.initial_data.get('images')[image]
                    images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='products/product_'+str(product.id), size=c_image.size)
                    product.images.add(images)
