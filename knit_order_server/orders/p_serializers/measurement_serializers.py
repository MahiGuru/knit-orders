from rest_framework import serializers
from ..p_models.measurments_model import MeasurementModel

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementModel
        fields = ('id', 'unit', 'blouse_opening', 'blouse_length', 'arm_hole_length', 'lower_bust_length', 'bust_length', 'shoulder_length', 'neck_front_length', 'neck_back_length', 'sleeve_length', 'sleeve_width_length')
    
    def validate(self, data):
        return data

    def create(self, validated_data):       
        ## Role data 
        measurement = MeasurementModel.objects.create(**validated_data)
        return measurement

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.size = validated_data.get('size', instance.size) 
        instance.code = validated_data.get('code', instance.code) 
        instance.save() 
        return instance