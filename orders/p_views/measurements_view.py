import csv
from django.conf import settings
from django.core.files import File
from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

from ..p_models.measurments_model import MeasurementModel
from ..p_serializers.measurement_serializers import MeasurementSerializer

import logging
logger = logging.getLogger(__name__)

class MeasurementsViewSet(viewsets.ModelViewSet):
    queryset = MeasurementModel.objects.all()
    serializer_class = MeasurementSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['unit', 'blouse_opening', 'blouse_length', 'arm_hole_length', 'lower_bust_length', 'bust_length', 'shoulder_length', 'neck_front_length', 'neck_back_length', 'sleeve_length', 'sleeve_width_length']
    
    filter_fields = ['unit', 'blouse_opening', 'blouse_length', 'arm_hole_length', 'lower_bust_length', 'bust_length', 'shoulder_length', 'neck_front_length', 'neck_back_length', 'sleeve_length', 'sleeve_width_length']
    
    def create(self, request, *args, **kwargs):  
        logger.info(" \n\n ----- Measurements CREATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES
            logger.info("Images length = {}".format(len(request.FILES)))

        measurements_serializer = MeasurementSerializer(data= request.data)
        if measurements_serializer.is_valid():
            measurements_serializer.save()
            logger.info({'MeasurementId':measurements_serializer.instance.id, 'status':'200 Ok'})
            logger.info("Measurements saved successfully")
            return Response({'MeasurementId':measurements_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            logger.info(measurements_serializer.errors)
            logger.info("Measurements save failed")
            return Response(measurements_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- Measurements UPDATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES
            logger.info("Images length = {}".format(len(request.FILES)))     
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info({'MeasurementId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("Measurements Updated successfully")
        return Response({'MeasurementId':serializer.instance.id}, status=status.HTTP_200_OK)
 
    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- Measurements DELETED initiated -----")
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete()
        logger.info("Measurements deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for e in instance.images.all():
            instance.images.remove(e)
            KImage.objects.get(id=e.id).delete()
            logger.info("Measurements Image deleted {}".format(e.id))


# ## USER CAN UPLOAD CATEGORY FROM CSV/EXCEL
# class CSVUploadCategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
     
#     parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

#     def create(self, request, *args, **kwargs):
#         logger.info(" \n\n ----- CSV CATEGORY CREATE initiated -----")

#         csvFile = ''
#         if request.FILES:
#             csvFile = request.FILES
#         results = []
#         for csv_file in request.FILES:
#             logger.info(" \n\n ----- CSV VENDOR CREATE initiated -----")
#             # with open(request.FILES[csv_file].name) as f:
#             decoded_file = request.FILES[csv_file].read().decode('utf-8').splitlines()
#             csv_reader = csv.DictReader(decoded_file)
#             for i, row in enumerate(csv_reader):
#                 if row:
#                     print(row)
#                     stitch_data = {}
#                     stitch_data['name'] = row.get('name')
#                     stitch_data['description'] = row.get('description') 
#                     if row.get("image"):
#                         with open(row.get('image'), 'rb') as f:
#                             stitch_data['images'] = {'images' : File(f) }                    
#                     measurements_serializer = CategorySerializer(data= stitch_data)
#                     measurements_serializer.is_valid(raise_exception=True)
#                     try:
#                         measurements_serializer.save()
#                         print("Saved Category")
#                         results.append({'MeasurementId':measurements_serializer.instance.id, "status":status.HTTP_201_CREATED})
#                     except Exception:
#                         print("Already has the Category")
#         return Response(results, status=status.HTTP_201_CREATED)

