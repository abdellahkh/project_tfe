from django.shortcuts import render
from .models import Voiture

# Create your views here.
def home(request):
    voitures = Voiture.objects.all()

    return render(request, 'home.html', {'voitures' :voitures})