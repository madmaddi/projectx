from rest_framework import serializers
from .models import Temperature, Window

class TemperatureSerializer(serializers.Serializer):

    class Meta:
        model = Temperature
        fields = ('id', 'pub_date', 'location', 'temperature', 'humidity')

    id = serializers.IntegerField(read_only=True)
    pub_date = serializers.DateTimeField(required=False)

    location = serializers.CharField(max_length = 3)

    temperature = serializers.DecimalField(max_digits=5, decimal_places=2)
    humidity = serializers.DecimalField(max_digits=5, decimal_places=2)


    def create(self, validated_data):
        return Temperature.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.temperature = validated_data.get('temperature', instance.temperature)
        instance.humidity = validated_data.get('humidity', instance.humidity)
        instance.save()
        return instance



class WindowSerializer(serializers.Serializer):

    class Meta:
        model = Window
        fields = ('id', 'pub_date', 'state')

    id = serializers.IntegerField(read_only=True)
    pub_date = serializers.DateTimeField(required=False)
    state = serializers.CharField(max_length = 5)


    def create(self, validated_data):
        return Window.objects.create(**validated_data)

