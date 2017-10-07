from rest_framework import serializers
#from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from .models import Temperature

class TemperatureSerializer(serializers.Serializer):

    class Meta:
        model = Temperature
        fields = ('id', 'temp_value', 'temp_type')


    id = serializers.IntegerField(read_only=True)
    temp_value = serializers.CharField(required=False, allow_blank=True, max_length=50)
    temp_type  = serializers.CharField(required=False, allow_blank=True, max_length=3)

    def create(self, validated_data):
        return Temperature.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.temp_value = validated_data.get('temp_value', instance.temp_value)
        instance.save()
        return instance
