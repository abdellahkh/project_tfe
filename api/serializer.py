from rest_framework import serializers
from car_dealer.models import Voiture, Member




class VoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voiture 
        fields = '__all__'



class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'