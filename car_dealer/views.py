from django.shortcuts import render, redirect
from .models import Voiture
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request):
    voitures = Voiture.objects.all()
    return render(request, 'home.html', {'voitures' :voitures})

def register_user(request):
    return render(request, 'register.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Vous etes connecte..."))
            return redirect('home')
        else:
            messages.success(request, ("Une erreur est survenue, veuillez reessayer..."))
            return redirect('login')

    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Vous avez ete deconnecte..."))
    return redirect('home')



def about(request):
    return render(request, 'about.html', {})
def allServices(request):
    return render(request, 'allServices.html', {})