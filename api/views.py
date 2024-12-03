from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from car_dealer.models import Voiture, Member
from .serializer import MemberSerializer, VoitureSerializer
from django.urls import reverse

@api_view(['GET'])
def get_voiture(request):
    voitures = Voiture.objects.all()
    serializer = VoitureSerializer(voitures, many=True)  
    return Response(serializer.data)



@api_view(['GET'])
def get_voiture_status(request, status):
    voitures = Voiture.objects.filter(status=status )
    serializer = VoitureSerializer(voitures, many=True)  
    return Response(serializer.data)

@api_view(['POST'])
def add_voiture(request):
    serializer = VoitureSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_users(request):
    members = Member.objects.all()
    serializer = MemberSerializer(members, many=True)  
    return Response(serializer.data)


@api_view(['GET'])
def api_root(request):
    return Response({
        'Liste des voitures': request.build_absolute_uri(reverse('get_voiture')),
        'Liste des membres': request.build_absolute_uri(reverse('get_users')),
        'Ajouter une voiture': request.build_absolute_uri(reverse('add_voiture')),
        'Voiture par statut': request.build_absolute_uri(reverse('get_voiture_status', args=['example_status'])),
    })