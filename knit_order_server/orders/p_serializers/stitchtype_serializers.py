from rest_framework import serializers
from ..p_models.stitch_types import StitchTypeModel
from ..p_models.image_model import KImage

class StitchTypeSerializer(serializers.ModelSerializer):
    
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StitchTypeModel
        fields = ('id', 'stitch_type', 'code', 'description', 'images')
    
    def get_images(self, obj):
        serializer = ImageSerializer(obj.images, many=True)
        return serializer.data 

    def validate(self, data):
        return data

    def create(self, validated_data):       
        ## Role data 
        measurement = StitchTypeModel.objects.create(**validated_data)
        return measurement

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.size = validated_data.get('size', instance.size) 
        instance.code = validated_data.get('code', instance.code) 
        instance.save() 
        return instance