from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from ..p_models.image_model import KImage
from ..p_models.order_model import Orders
from ..p_serializers.order_serializer import OrderSerializer

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend
from ..paginations import LinkSetPagination 

import logging
logger = logging.getLogger(__name__)
 

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['id', 'stitch_type','isClothAvailable', 'isStitchType', 'expected_date', 'extra_notes', 'images', 'measurements', 'cloth_size']
    
    pagination_class = LinkSetPagination

    filter_fields = ['id', 'stitch_type','isClothAvailable', 'isStitchType', 'expected_date', 'extra_notes', 'images', 'measurements', 'cloth_size']
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
    
    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- Order CREATE initiated -----")
        order = self.prepareOrderData(request.data)
        images = {}
        if request.FILES:
            images = request.FILES
        logger.debug(order)
        logger.debug("Data prepared. Sending data to the serializer ")
        order_serializer = OrderSerializer(data= {'data':request.data, 'order':order['data'], 'order_relations':order['additional_data'], 'images': images})
        order_serializer.is_valid(raise_exception=True)
        order_serializer.save()
        logger.debug({'OrderId':order_serializer.instance.id, "status":200})
        logger.debug("Order saved successfully!!!")
        return Response({'orderId':order_serializer.instance.id}, status=status.HTTP_201_CREATED)
        
    def update(self, request, *args, **kwargs):
        order = self.prepareOrderData(request.data)
        if request.FILES:
            order.additional_data['images'] = request.FILES
        serializer = self.get_serializer(self.get_object(), data= {'data':request.data, 'order':order['data'], 'order_relations':order['additional_data']}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for e in instance.images.all():
            instance.images.remove(e)
            KImage.objects.get(id=e.id).delete()
    
    #======================== CREATE ORDER ========================#
    def prepareOrderData(self, order_input, instance=None):
        order = {}
        order['stitch_type'] = order_input.get('stitch_type')
        order['isClothAvailable'] = order_input.get('isClothAvailable')
        order['isStitchType'] = order_input.get('isStitchType')
        order['expected_date'] = order_input.get('expected_date')
        order['extra_notes'] = order_input.get('extra_notes')
        order['measurements'] = order_input.get('measurements')
        order['cloth_size'] = order_input.get('cloth_size')
        order['user'] = order_input.get('user')

        # Many to Many fields
        additional_data = {}
        order['images'] = order_input.get('images') 
        additional_data['sizes'] = order_input.get('sizes')
        additional_data['cloth_size'] = order_input.get('cloth_size')
        return {'data': order, 'additional_data': additional_data}