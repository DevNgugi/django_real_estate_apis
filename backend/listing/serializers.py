from dataclasses import field
from rest_framework import serializers
from .models import Listing 


class ListingSerializer(serializers.Serializer):
    class Meta:
        model = Listing
        fields = '__all__'
