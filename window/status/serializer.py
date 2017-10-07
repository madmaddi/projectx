from rest_framework import serializers
#from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from .models import Temperature

class TemperatureSerializer(serializers.Serializer):
    class Meta:
        model = Temperature
        fields = ('id', 'temp_value', 'temp_type', 'linenos', 'language', 'style')

    """
    id = serializers.IntegerField(read_only=True)
    temp_value = serializers.CharField(required=False, allow_blank=True, max_length=50)
    temp_type  = serializers.CharField(required=False, allow_blank=True, max_length=3)
    #title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    #code = serializers.CharField(style={'base_template': 'textarea.html'})
    #linenos = serializers.BooleanField(required=False)
    #language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    #style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):

        #Create and return a new `Snippet` instance, given the validated data.

        return Temperature.objects.create(**validated_data)


    def update(self, instance, validated_data):

        #Update and return an existing `Snippet` instance, given the validated data.

        instance.title = validated_data.get('pub_date', instance.pub_date)
        instance.save()
        return instance
    """