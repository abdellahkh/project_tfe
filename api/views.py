from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from car_dealer.models import Voiture
from .serializer import VoitureSerializer

@api_view(['GET'])
def get_voiture(request):
    voitures = Voiture.objects.all()
    serializer = VoitureSerializer(voitures, many=True)  
    return Response(serializer.data)

@api_view(['GET'])
def get_voiture_status(request, pk):
    voitures = Voiture.objects.filter(status=pk )
    serializer = VoitureSerializer(voitures, many=True)  
    return Response(serializer.data)

@api_view(['POST'])
def add_voiture(request):
    serializer = VoitureSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
