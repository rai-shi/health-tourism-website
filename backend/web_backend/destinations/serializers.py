from rest_framework import serializers
from .models import *


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'


class DestinationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'