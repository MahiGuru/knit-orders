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

from ..p_models.stitch_types import StitchTypeModel
from ..p_serializers.stitchtype_serializers import StitchTypeSerializer

import logging
logger = logging.getLogger(__name__)

class StitchTypeViewSet(viewsets.ModelViewSet):
    queryset = StitchTypeModel.objects.all()
    serializer_class = StitchTypeSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['stitch_type', 'code', 'description']
    
    filter_fields = ['stitch_type', 'code', 'description']
    
    def create(self, request, *args, **kwargs):  
        logger.info(" \n\n ----- STITCH TYPE CREATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES
            logger.info("Images length = {}".format(len(request.FILES)))

        stitchtype_serializer = StitchTypeSerializer(data= request.data)
        if stitchtype_serializer.is_valid():
            stitchtype_serializer.save()
            logger.info({'stitchtypeId':stitchtype_serializer.instance.id, 'status':'200 Ok'})
            logger.info("StichType saved successfully")
            return Response({'stitchtypeId':stitchtype_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            logger.info(stitchtype_serializer.errors)
            logger.info("StichType save failed")
            return Response(stitchtype_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- StichType UPDATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES
            logger.info("Images length = {}".format(len(request.FILES)))     
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info({'stitchtypeId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("StichType Updated successfully")
        return Response({'stitchtypeId':serializer.instance.id}, status=status.HTTP_200_OK)
 
    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- StichType DELETED initiated -----")
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete()
        logger.info("StichType deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for e in instance.images.all():
            instance.images.remove(e)
            KImage.objects.get(id=e.id).delete()
            logger.info("StichType Image deleted {}".format(e.id))


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
#                     stitchtype_serializer = CategorySerializer(data= stitch_data)
#                     stitchtype_serializer.is_valid(raise_exception=True)
#                     try:
#                         stitchtype_serializer.save()
#                         print("Saved Category")
#                         results.append({'stitchtypeId':stitchtype_serializer.instance.id, "status":status.HTTP_201_CREATED})
#                     except Exception:
#                         print("Already has the Category")
#         return Response(results, status=status.HTTP_201_CREATED)

