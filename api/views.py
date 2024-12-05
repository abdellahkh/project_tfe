from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from car_dealer.models import Voiture, Member, Demande, Service, Vente
from .serializer import VoitureSerializer, MemberSerializer, DemandeSerializer, ServiceSerializer, VenteSerializer
from django.urls import reverse


@api_view(['GET'])
def api_root(request):
    return Response({
        'Liste des voitures': request.build_absolute_uri(reverse('get_voiture')),
        'Voitures par statut': request.build_absolute_uri(reverse('get_voiture_status', args=['example_status'])),
        'Ajouter une voiture': request.build_absolute_uri(reverse('add_voiture')),
        'Liste des membres': request.build_absolute_uri(reverse('get_users')),
        'Liste des demandes': request.build_absolute_uri(reverse('get_demandes')),
        'Demandes par statut': request.build_absolute_uri(reverse('get_demandes_status', args=['example_status'])),
        'Liste des services': request.build_absolute_uri(reverse('get_services')),
        'Liste des ventes': request.build_absolute_uri(reverse('get_ventes')),
    })


@api_view(['GET'])
def get_voiture(request):
    voitures = Voiture.objects.all()
    serializer = VoitureSerializer(voitures, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_voiture_status(request, status):
    voitures = Voiture.objects.filter(status=status)
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
def get_demandes(request):
    demandes = Demande.objects.all()
    serializer = DemandeSerializer(demandes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_demandes_status(request, status):
    demandes = Demande.objects.filter(status=status)
    serializer = DemandeSerializer(demandes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_services(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_ventes(request):
    ventes = Vente.objects.all()
    serializer = VenteSerializer(ventes, many=True)
    return Response(serializer.data)
