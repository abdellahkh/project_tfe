from rest_framework import serializers
from car_dealer.models import Voiture




class VoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voiture 
        fields = '__all__'