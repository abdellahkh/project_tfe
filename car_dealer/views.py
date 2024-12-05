import datetime
from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import ImageVoiture, Notes, Review, Service, UserWishlist, Vente, Voiture, Member, Demande, VoitureSoumisse
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import DemandeContactVoitureMembre, ImageVoitureForm, ReviewForm, SignUpForm, UserUpdateForm, DemandeDeplacement, DemandeControlTech, DemandeControlTechMembre, DemandeDeplacementMembre, DemandeSortieDeFourriereMembre, DemandeSortieDeFourriere, VenteVehicule, VenteVehiculeMembre, VoitureForm
from django import forms
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.views import View
from car_dealer import models
from django.utils.translation import gettext as _

from django.http import FileResponse, HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.contrib.auth.decorators import login_required

def home(request):
    voitures = Voiture.objects.filter(status='Available').prefetch_related('images').order_by('-date_poste')[:6]
    services = Service.objects.filter(is_available=True)

    wishlist_voiture_ids = []  # Initialize as an empty list
    if request.user.is_authenticated:
        wishes = UserWishlist.objects.filter(user=request.user)
        wishlist_voiture_ids = wishes.values_list('voiture__id', flat=True)

    var = _("Les meilleurs services d'accompagnement")

    return render(request, 'home.html', {
        'voitures': voitures, 
        'services': services,
        'wishlist_voiture_ids': wishlist_voiture_ids,  # Add this line
        'var': var
    })

def activate(request, uidb64, token):
    # User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Member.objects.get(id=uid)
    except Member.DoesNotExist:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Merci d\'avoir validé votre compte, vous pouvez maintenant vous connecter.')
        return redirect('login')
    else:
        messages.error(request, "Le lien d\'activation n'est pas valide!")

    return redirect('home')

# 
from django.core.paginator import Paginator

from datetime import timedelta
from django.db.models import Count, Sum
from django.utils.timezone import now
from django.core.paginator import Paginator
import json

from datetime import timedelta
from django.db.models import Count, Sum
from django.utils.timezone import now
from django.core.paginator import Paginator

def dashboard(request):
    # Récupération des filtres
    genre_filter = request.GET.get('genre', '')
    status_voiture_filter = request.GET.get('status_voiture', '')
    status_filter = request.GET.get('status', '')
    service_filter = request.GET.get('service', '')
    status_vente_filter = request.GET.get('status_vente', '')  # Nouveau filtre pour le statut des ventes

    # Récupération des données
    ventes = Vente.objects.all().order_by('-date')
    voitures = Voiture.objects.all().order_by('-date_poste')
    demandes = Demande.objects.all().order_by('-date')

    # Application des filtres
    if genre_filter:
        ventes = ventes.filter(genre=genre_filter)
    if status_voiture_filter:
        voitures = voitures.filter(status=status_voiture_filter)
    if status_filter:
        demandes = demandes.filter(status=status_filter)
    if service_filter:
        demandes = demandes.filter(service_id=service_filter)
    if status_vente_filter:
        ventes = ventes.filter(paid=status_vente_filter)

    # Pagination
    voiture_paginator = Paginator(voitures, 6)
    ventes_paginator = Paginator(ventes, 6)
    demandes_paginator = Paginator(demandes, 6)

    page_number_voitures = request.GET.get('page_voitures')
    page_number_ventes = request.GET.get('page_ventes')
    page_number_demandes = request.GET.get('page_demandes')

    voitures_page_obj = voiture_paginator.get_page(page_number_voitures)
    ventes_page_obj = ventes_paginator.get_page(page_number_ventes)
    demandes_page_obj = demandes_paginator.get_page(page_number_demandes)

    # Statistiques globales
    total_voitures_vendues = Vente.objects.filter(voiture_id__isnull=False).count()
    ventes_semaine = Vente.objects.filter(date__gte=now() - timedelta(days=7)).count()
    total_revenus = Vente.objects.aggregate(Sum('montant_total'))['montant_total__sum'] or 0

    # Statistiques pour les employés
    voitures_disponibles = Voiture.objects.filter(status='Available').count()
    demandes_attente = Demande.objects.filter(status='Actif').count()
    total_voitures = Voiture.objects.count()
    pourcentage_voitures_vendues = round((total_voitures_vendues / total_voitures) * 100, 2) if total_voitures > 0 else 0

    # Comparaison des ventes hebdomadaires
    ventes_semaine_derniere = Vente.objects.filter(
        date__gte=now() - timedelta(days=14),
        date__lt=now() - timedelta(days=7)
    ).count()
    progression_semaine = (
        round(((ventes_semaine - ventes_semaine_derniere) / ventes_semaine_derniere) * 100, 2)
        if ventes_semaine_derniere > 0 else 0
    )

    # Graphiques
    sales_by_service = Vente.objects.values('demande_id__service__nom').annotate(count=Count('id'))
    sales_by_service_labels = [item['demande_id__service__nom'] for item in sales_by_service]
    sales_by_service_data = [item['count'] for item in sales_by_service]

    requests_by_service = Demande.objects.values('service__nom').annotate(count=Count('id'))
    requests_by_service_labels = [item['service__nom'] for item in requests_by_service]
    requests_by_service_data = [item['count'] for item in requests_by_service]

    # Liste des statuts et services pour les filtres
    voiture_status = Voiture.STATUS_CHOICES
    demande_status = [status[0] for status in Demande.STATUS_OPTIONS]
    demande_services = Service.objects.all()
    vente_status = Vente.PAIEMENT_CHOICES  # Liste des choix de statut de paiement

    return render(request, 'dashboard.html', {
        'ventes': ventes_page_obj,
        'voitures': voitures_page_obj,
        'demandes': demandes_page_obj,
        'total_voitures_vendues': total_voitures_vendues,
        'ventes_semaine': ventes_semaine,
        'total_revenus': total_revenus,
        'voitures_disponibles': voitures_disponibles,
        'demandes_attente': demandes_attente,
        'pourcentage_voitures_vendues': pourcentage_voitures_vendues,
        'progression_semaine': progression_semaine,
        'sales_by_service_labels': json.dumps(sales_by_service_labels),
        'sales_by_service_data': json.dumps(sales_by_service_data),
        'requests_by_service_labels': json.dumps(requests_by_service_labels),
        'requests_by_service_data': json.dumps(requests_by_service_data),
        'voiture_status': voiture_status,
        'demande_status': demande_status,
        'demande_services': demande_services,
        'vente_status': vente_status,  # Liste des statuts de vente pour le filtre
        'status_voiture_filter': status_voiture_filter,
        'status_filter': status_filter,
        'service_filter': service_filter,
        'genre_filter': genre_filter,
        'status_vente_filter': status_vente_filter,  # Ajout du filtre actuel pour le statut de vente
    })


    
def demandeDetails(request, demande_id):
    demand = Demande.objects.get(id=demande_id)
    notes = Notes.objects.filter(demande_id = demande_id).order_by('-date')
    return render(request, 'demandDetail.html', {'demand' : demand, 'notes': notes})

def activateEmail(request, user, to_email):
    mail_subject = "Activez votre compte."
    message = render_to_string("activate_account.html",{
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'

    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Cher {user}, verifie votre boite de messagerie {to_email} et cliquez sur \
                        le lien d\'activation pour confirmer l\'inscription.')
    else:
        messages.error(request, f'Une erreur est survenue. Verifie l\'adresse: {to_email}.')

def serviceEmailToAdmin(request, user, serviceNom, form, to_email, voiture):
    mail_subject = "Nouvelle demande de service"
    first_name = form.cleaned_data.get('first_name', '')
    last_name = form.cleaned_data.get('last_name', '')
    email = form.cleaned_data.get('email', '')
    phone = form.cleaned_data.get('phone', '')
    message = render_to_string("email_template/demande_submit.html", {
        'user': user,  # Use dictionary syntax
        'domain': get_current_site(request).domain,
        'protocol': 'https' if request.is_secure() else 'http',
        'service': serviceNom,
        'first_name': first_name,  
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'voiture': voiture,
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    first_name = first_name
    if email.send():
        messages.success(request, f'Cher {first_name if first_name else user.username}, votre demande a bien été soumise, vous allez être recontacté sous peu.')
    else:
        messages.error(request, f'Une erreur est survenue. Veuillez réessayer plus tard.')



def serviceEmailToAdminFromMembre(request, user, serviceNom, form, to_email, autre):
    mail_subject = "Nouvelle demande de service"
    message = render_to_string("email_template/demande_submit.html", {
        'user': user,  # Use dictionary syntax
        'domain': get_current_site(request).domain,
        'protocol': 'https' if request.is_secure() else 'http',
        'service': serviceNom,
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    first_name = user
    if email.send():
        messages.success(request, f'Cher {first_name}, votre demande a bien été soumise, vous allez être recontacté sous peu.')
    else:
        messages.error(request, f'Une erreur est survenue. Veuillez réessayer plus tard.')

def venteEmailToAdminFromMembre(request, user, serviceNom, product, to_email, montant_accomte):
    mail_subject = "Reservation voiture"
    message = render_to_string("email_template/reservation_submit.html", {
        'user': user,  # Use dictionary syntax
        'domain': get_current_site(request).domain,
        'protocol': 'https' if request.is_secure() else 'http',
        'service': serviceNom,
        'id': product.id,
        'marque': product.marque,
        'modele': product.modele,
        'annee' : product.annee_fabrication,
        'montant_accomte': montant_accomte
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    first_name = user
    if email.send():
        messages.success(request, f'Cher {first_name}, merci pour votre paiement.')
    else:
        messages.error(request, f'Une erreur est survenue. Veuillez réessayer plus tard.')



def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(request, "Inscription réussie! Un email d'activation vous a été envoyé.")
            return redirect('home')
        else:
            messages.error(request, "Des erreurs sont survenues lors de l'inscription. Veuillez vérifier les champs.")
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})



def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Vérification des champs vides
        if not username or not password:
            messages.error(request, "Les champs nom d'utilisateur et mot de passe sont obligatoires.")
            return redirect('login')

        # Vérification de l'existence de l'utilisateur
        try:
            user = Member.objects.get(username=username)  # Utilisation de Member au lieu de User
        except Member.DoesNotExist:
            messages.error(request, "Ce nom d'utilisateur n'existe pas.")
            return redirect('login')

        # Authentification de l'utilisateur
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Vous êtes connecté.")
            return redirect('home')
        else:
            messages.error(request, "Le mot de passe est incorrect.")
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
    services = Service.objects.all()
    reviews = Review.objects.all()
    form = ReviewForm()  # Instancier le formulaire
    return render(request, 'allServices.html', { 
        'services': services, 
        'reviews': reviews, 
        'form': form  # Passer le formulaire au template
    })

def ajouter_commentaire(request, service_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)  # Ne pas enregistrer tout de suite
            review.user_id = request.user  # Associer l'utilisateur connecté
            review.service_id = Service.objects.get(id=service_id)  # Associer le service
            review.save()
            return redirect('services')  # Rediriger après la création
    else:
        form = ReviewForm()
    return redirect('services')

def allVoitures(request):
    voitures = Voiture.objects.all()
    wishlist_voiture_ids = [] 
    if request.user.is_authenticated:  # Check if the user is authenticated
        wishes = UserWishlist.objects.filter(user=request.user)
        wishlist_voiture_ids = wishes.values_list('voiture__id', flat=True)

    # Filtrage par marque, carburant, transmission et status
    marque = request.GET.get('marque')
    carburant = request.GET.get('carburant')
    transmission = request.GET.get('transmission')
    status = request.GET.get('status')  # Nouveau filtre

    if marque:
        voitures = voitures.filter(marque__nom=marque)

    if carburant:
        voitures = voitures.filter(carburant=carburant)

    if transmission:
        voitures = voitures.filter(transmission=transmission)

    if status:
        voitures = voitures.filter(status=status)  # Application du filtre status

    # Récupération des marques, carburants, transmissions et statuts distincts
    marques_disponibles = Voiture.objects.order_by('marque__nom').values_list('marque__nom', flat=True).distinct()
    carburants_disponibles = Voiture.objects.order_by('carburant').values_list('carburant', flat=True).distinct()
    transmissions_disponibles = Voiture.objects.order_by('transmission').values_list('transmission', flat=True).distinct()
    status_disponibles = Voiture.objects.order_by('status').values_list('status', flat=True).distinct()  # Nouveaux statuts

    return render(request, 'allVoitures.html', {
        'voitures': voitures,
        'marques_disponibles': marques_disponibles,
        'carburants_disponibles': carburants_disponibles,
        'transmissions_disponibles': transmissions_disponibles,
        'status_disponibles': status_disponibles,  # Ajout des statuts au contexte
        'wishlist_voiture_ids': wishlist_voiture_ids
    })


def saleAddCar(request):
    return render (request, 'dashboardAddVoiture.html')

def voiture(request, pk):
    voiture = Voiture.objects.prefetch_related('images').get(id=pk)
    return render(request, 'voiture.html', {'voiture': voiture})


def service(request, service_id):
    submitted = False
    service = Service.objects.get(id=service_id)
    user = request.user
    service_nom = service.nom
    form = None
    mail_to = 'etu.abkh@gmail.com'
    if service.nom in ['Déplacement de Véhicule Longue Distance', 'Déplacement de Véhicule Courte Distance']:
        if request.user.is_authenticated:
            if request.method == 'POST':
                
                form = DemandeDeplacementMembre(request.POST)
                form.instance.service = service
                form.instance.member = request.user
                if form.is_valid():
                    form.save()
                    # serviceEmailToAdminFromMembre(request, user, service_nom, form, mail_to, None)
                    return redirect('home')
                else:
                    print(form.errors)
                    messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
            else:
                form = DemandeDeplacementMembre()
                if 'submitted' in request.GET:
                    submitted = True
        else:
            if request.method == 'POST':
                form = DemandeDeplacement(request.POST)
                form.instance.service = service
                if form.is_valid():
                    form.save()
                    user = {
                        'first_name': form.cleaned_data['first_name'],
                        'last_name': form.cleaned_data['last_name'],
                        'phone': form.cleaned_data['phone'],
                        'email': form.cleaned_data['email'],
                    }
                    # serviceEmailToAdmin(request, user, service_nom, form, mail_to, None)
                    return redirect('home')
                else:
                    print(form.errors)
                    messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
            else:
                form = DemandeDeplacement()
                if 'submitted' in request.GET:
                    submitted = True

    elif service.nom in ['Passage au controle technique de vente', 'Passage au controle technique annuel']:
        mail_to = 'etu.abkh@gmail.com'
        
        if request.user.is_authenticated:
            if request.method == 'POST':
                form = DemandeControlTechMembre(request.POST)
                form.instance.service = service
                form.instance.member = request.user
                if form.is_valid():
                    form.save()
                    # serviceEmailToAdminFromMembre(request, user, service_nom, form, mail_to, None)
                    return redirect('home')
                else:
                    print(form.errors)
                    messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
            else:
                
                form = DemandeControlTechMembre() # => ce formulaire ne s'affiche pas dans mon html
                if 'submitted' in request.GET:
                    submitted = True
        else:
            if request.method == 'POST':
                form = DemandeControlTech(request.POST)
                form.instance.service = service
                form.instance.member = request.user.id
                if form.is_valid():
                    form.save()
                    user = {
                        'first_name': form.cleaned_data['first_name'],
                        'last_name': form.cleaned_data['last_name'],
                        'phone': form.cleaned_data['phone'],
                        'email': form.cleaned_data['email'],
                    }
                    # serviceEmailToAdmin(request, user, service_nom, form, mail_to, None)
                    return redirect('home')
                else:
                    print(form.errors)
                    messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
            else:
                form = DemandeControlTech()
                if 'submitted' in request.GET:
                    submitted = True

    elif service.nom == 'Service de Sortie de Fourrière':
        if request.user.is_authenticated:
            if request.method == 'POST':
                form = DemandeSortieDeFourriereMembre(request.POST)
                form.instance.service = service
                form.instance.member = request.user
                if form.is_valid():
                    form.save()
                    # serviceEmailToAdminFromMembre(request, user, service_nom, form, mail_to, None)
                    return redirect('home')
                else:
                    print(form.errors)
                    messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
            else:
                form = DemandeSortieDeFourriereMembre()
                if 'submitted' in request.GET:
                    submitted = True
        else:
            if request.method == 'POST':
                form = DemandeSortieDeFourriere(request.POST)
                form.instance.service = service
                form.instance.member = request.user.id
                voiture = None
                if form.is_valid():
                    user = {
                        'first_name': form.cleaned_data['first_name'],
                        'last_name': form.cleaned_data['last_name'],
                        'phone': form.cleaned_data['phone'],
                        'email': form.cleaned_data['email'],
                    }
                    form.save()
                    # serviceEmailToAdmin(request, user, service_nom, form, mail_to, voiture)
                    return redirect('home')
                else:
                    print(form.errors)
                    messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
            else:
                form = DemandeSortieDeFourriere()
                if 'submitted' in request.GET:
                    submitted = True

    elif service.nom == 'Service d\'Achat de Véhicule':
        if request.user.is_authenticated:
            if request.method == 'POST':
                form = VenteVehiculeMembre(request.POST)
                form.instance.service = service
                form.instance.user_id = request.user
                if form.is_valid():
                    form.save()
                    voiture = {
                        'marque': form.cleaned_data['marque'],
                        'modele': form.cleaned_data['modele'],
                        'annee_fabrication': form.cleaned_data['annee_fabrication'],
                        'carburant': form.cleaned_data['carburant'],
                        'transmission': form.cleaned_data['transmission'],
                        'prix': form.cleaned_data['prix'],
                    }
                    # serviceEmailToAdmin(request, user, service_nom, form, mail_to, voiture)
                    return redirect('home')
                else:
                    print(form.errors)
                    messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
            else:
                form = VenteVehiculeMembre()
                if 'submitted' in request.GET:
                    submitted = True
        else:
            if request.method == 'POST':
                form = VenteVehicule(request.POST)
                form.instance.service = service
                if form.is_valid():
                    user = {
                        'first_name': form.cleaned_data['first_name'],
                        'last_name': form.cleaned_data['last_name'],
                        'phone': form.cleaned_data['phone'],
                        'email': form.cleaned_data['email'],
                    }
                    voiture = {
                        'marque': form.cleaned_data['marque'],
                        'modele': form.cleaned_data['modele'],
                        'annee_fabrication': form.cleaned_data['annee_fabrication'],
                        'carburant': form.cleaned_data['carburant'],
                        'transmission': form.cleaned_data['transmission'],
                        'prix': form.cleaned_data['prix'],
                    }
                    form.save()
                    # serviceEmailToAdmin(request, user, service_nom, form, mail_to, voiture)
                    return redirect('home')
                else:
                    print(form.errors)
                    messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
            else:
                form = VenteVehicule()
                if 'submitted' in request.GET:
                    submitted = True

    elif service.nom == 'Contact pour information voiture':
        if request.user.is_authenticated:
            if request.method == 'POST':
                form = DemandeContactVoitureMembre(request.POST)
                form.instance.service = service
                form.instance.member = request.user
                if form.is_valid():
                    form.save()
                    # serviceEmailToAdminFromMembre(request, user, service_nom, form, mail_to)
                    return redirect('home')
                else:
                    print(form.errors)
                    messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
            else:
                form = DemandeContactVoitureMembre()
                if 'submitted' in request.GET:
                    submitted = True
        else:
            if request.method == 'POST':
                form = DemandeContactVoitureMembre(request.POST)
                form.instance.service = service
                form.instance.member = request.user.id
                if form.is_valid():
                    user = {
                        'first_name': form.cleaned_data['first_name'],
                        'last_name': form.cleaned_data['last_name'],
                        'phone': form.cleaned_data['phone'],
                        'email': form.cleaned_data['email'],
                    }
                    form.save()
                    # serviceEmailToAdmin(request, user, service_nom, form, mail_to)
                    return redirect('home')
                else:
                    print(form.errors)
                    messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
            else:
                form = VenteVehicule()
                if 'submitted' in request.GET:
                    submitted = True


    return render(request, 'formulaire/service_demande.html', {'form': form, 'submitted': submitted, 'service': service})




def contact_vehicule(request, voiture_id):
    voiture = Voiture.objects.prefetch_related('images').get(id=voiture_id)
    service_nom = 'Contact pour information voiture'
    mail_to = 'etu.abkh@gmail.com'
    service = Service.objects.get(nom=service_nom)

    if request.method == 'POST':
        form = DemandeContactVoitureMembre(request.POST)
        if request.user.is_authenticated:
            form.instance.member = request.user
        form.instance.service = service
        form.instance.voiture = voiture
        form.instance.genre = "Info"
        if form.is_valid():
            if request.user.is_authenticated:
                # serviceEmailToAdminFromMembre(request, request.user, service_nom, form, mail_to, None)
                form.save()
            else:
                user = {
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'phone': form.cleaned_data['phone'],
                    'email': form.cleaned_data['email'],
                }
                # serviceEmailToAdmin(request, user, service_nom, form, mail_to)
                form.save()
            return redirect('home')
        else:
            messages.error(request, "Hmm, une erreur s'est produite. Veuillez réessayer plus tard.")
    else:
        form = DemandeContactVoitureMembre()

    return render(request, 'formulaire/contact_vehicule.html', {'voiture': voiture, 'service': service, 'form': form})



def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    
    demandes = Demande.objects.filter(member=user).order_by('-date')
    voitureSoumisses = VoitureSoumisse.objects.filter(user_id=user)
    toutesDemandes = Demande.objects.all().order_by('-date')
    ventes = Vente.objects.filter(user_id=user)
    
    # Vérification explicite de la visibilité des notes
    notes = Notes.objects.filter(customer_visible=True).order_by('-date')

    # Wishlist
    wishlist, created = UserWishlist.objects.get_or_create(user=request.user)
    wishlist_voitures = wishlist.voiture.all()

    wishlist_voiture_ids = []
    if request.user.is_authenticated:
        wishes = UserWishlist.objects.filter(user=request.user)
        wishlist_voiture_ids = wishes.values_list('voiture__id', flat=True)

    return render(request, "profile_view.html", {
        'user': user,
        'demandes': demandes,
        'voitureSoumisses': voitureSoumisses,
        'toutesDemandes': toutesDemandes,
        'ventes': ventes,
        'wishlist_voiture_ids': wishlist_voiture_ids,
        'wishlist_voitures': wishlist_voitures,
        'notes': notes
    })





def profileEdit(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)  # Utilisez le même nom 'form' ici
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'{user_form.username}, Votre profil a bien été modifié')
            return redirect("profile_view", user_form.username)
        else:
            # Affichez le formulaire et les erreurs sur la console
            print(form.errors)
            messages.error(request, f'Hmm une erreur s\'est produite, veuillez réessayer plus tard')

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(
            request=request,
            template_name="profile.html",
            context={"form": form}  # Utilisez le même nom 'form' ici
        )
    return redirect("home")

def vendre(request):
    service = Service.objects.get(id=3)
    mail_to = 'etu.abkh@gmail.com'
    service_nom = ''
    if request.user.is_authenticated:
        if request.method == 'POST':
                
            form = VenteVehicule(request.POST)
            form.instance.service = service
            if form.is_valid():
                form.save()
                # serviceEmailToAdminFromMembre(request, user, service_nom, form, mail_to)
                return redirect('home')
            else:
                print(form.errors)
                messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
        else:
            form = VenteVehicule()
            if 'submitted' in request.GET:
                submitted = True
    else:
        if request.method == 'POST':
            form = VenteVehicule(request.POST)
            form.instance.service = service
            if form.is_valid():
                form.save()
                user = {
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'phone': form.cleaned_data['phone'],
                    'email': form.cleaned_data['email'],
                }
                # serviceEmailToAdmin(request, user, service_nom, form, mail_to)
                return redirect('home')
            else:
                print(form.errors)
                messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
        else:
            form = VenteVehicule()
            if 'submitted' in request.GET:
                submitted = True
    return render(request, 'formulaire/vendre.html', {})


def vente_details(request, vente_id):
    vente = Vente.objects.get(id=vente_id)
    notes = Notes.objects.filter(vente_id=vente_id).order_by('-date')
    notesDemande = []  # Initialize notesDemande as an empty list

    if vente.demande_id:
        notesDemande = Notes.objects.filter(demande_id=vente.demande_id).order_by('-date')

    return render(request, "vente_details.html", {"vente": vente, "notes": notes, "notesDemande": notesDemande})

def vente_payer(request, vente_id):
    vente = Vente.objects.get(id=vente_id)
    vente.voiture_id.status = 'ready'
    vente.voiture_id.save()  
    return redirect('dashboard')


def ajouter_note(request, vente_id):
    vente = get_object_or_404(Vente, pk=vente_id)

    if request.method == 'POST':
        contenu = request.POST.get('contenu', '')  # Récupère le contenu de la note
        customer_visible = request.POST.get('customer_visible') == 'on'  # Récupère l'état de la checkbox
        Notes.objects.create(
            user_id=request.user,  # Assurez-vous que `request.user` est une instance valide
            vente_id=vente,
            contenu=contenu,
            customer_visible=customer_visible
        )
        return redirect('vente_details', vente_id=vente.id)  # Redirection vers la page de détails de la vente

    return redirect('vente_details', vente_id=vente.id)

def ajouter_note_demande(request, demande_id):
    demande = get_object_or_404(Demande, pk=demande_id)

    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        customer_visible = request.POST.get('customer_visible') == 'on'
        Notes.objects.create(
            user_id=request.user,  
            demande_id=demande,
            contenu=contenu,
            customer_visible=customer_visible
        )
        return redirect('demande_details', demande_id=demande.id)  #

    return redirect('demande_details', demande_id=demande.id)

def ajouter_note_vente(request, vente_id):
    vente = get_object_or_404(Vente, pk=vente_id)

    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        customer_visible = request.POST.get('customer_visible') == 'on'
        Notes.objects.create(
            user_id=request.user,  
            vente_id=vente,
            contenu=contenu,
            customer_visible=customer_visible
        )
        return redirect('vente_details', demande_id=vente.id)  #

    return redirect('vente_details', demande_id=vente.id)

def startVente(request, demande_id):
    demande = get_object_or_404(Demande, pk=demande_id)
    prix = request.POST.get('contenu')
    
    try:
        prix = float(prix)  
        prix_min = float(demande.voiture.prix_min)  

        if prix >= prix_min:
            vente = Vente.objects.create(
                genre='Vente',
                paid='no',
                demande_id=demande,
                user_id=demande.member,
                voiture_id=demande.voiture,
                montant_total=prix,
                montant_acompte=prix * 0.1,
            )

            demande.status = 'En preparation' 
            demande.save()
            notes = Notes.objects.filter(demande_id = demande_id)
            for note in notes:
                note.vente_id = vente
                note.save()
            return redirect('home')  
        else:
            messages.error(request, 'Prix trop bas, le prix min est ' + str(prix_min))  # Add request object and convert prix_min to string
            return redirect('demande_details', demande_id=demande.id)  # Redirect back to demand details

    except ValueError:
        messages.error(request, 'Veuillez entrer un prix valide.')
        return redirect('demande_details', demande_id=demande.id)


def startVenteService(request, demande_id):
    demande = get_object_or_404(Demande, pk=demande_id)
    prix = request.POST.get('contenu')
    try:
        prix = float(prix)  # Convert prix to a float

        if prix > 0:  # Add validation to ensure the price is positive
            Vente.objects.create(
                genre='Service',
                paid='no',
                demande_id=demande,
                user_id=demande.member,
                montant_total=prix,
            )
            
            demande.status = 'En preparation'
            demande.save()
            return redirect('dashboard')
        else:
            messages.error(request, 'Le prix doit être supérieur à zéro.')
            return redirect('demande_details', demande_id=demande.id)

    except ValueError:
        messages.error(request, 'Veuillez entrer un prix valide.')
        return redirect('demande_details', demande_id=demande.id)

def annuleVente(request, vente_id):
    if request.method == "POST":
        vente = get_object_or_404(Vente, pk=vente_id)
        raison = request.POST.get('raison', '').strip()  # Utiliser 'raison', comme dans le formulaire
        
        if raison:
            Notes.objects.create(
                user_id=request.user,
                vente_id=vente,
                contenu=f"Demande d'annulation par le client : {raison}"
            )
            messages.success(request, "Votre demande d'annulation a été soumise avec succès.")
        else:
            messages.error(request, "Vous devez fournir une raison pour l'annulation.")
        
        # Reste sur la même page
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.error(request, "Méthode non autorisée.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    

def annuler_vente_admin(request, vente_id):
    vente = get_object_or_404(Vente, pk=vente_id)
    vente.paid = 'cancelled'
    vente.save()
    voiture = get_object_or_404(Voiture, pk=vente.voiture_id.id)
    voiture.status = 'Available'
    voiture.save()
    Notes.objects.create(
                user_id=request.user,
                vente_id=vente,
                contenu=f"Annulation valider par : {request.user}"
            )
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
def voitureEdit(request, voiture_id):
    voiture = get_object_or_404(Voiture, pk=voiture_id)

    if request.method == "POST":
        form = VoitureForm(request.POST, instance=voiture)
        if form.is_valid():
            form.save()
            messages.success(request, "La voiture a été mise à jour avec succès.")
            return redirect('voitureEdit', voiture_id=voiture.id)  # Redirige vers la même page pour revoir les changements
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = VoitureForm(instance=voiture)

    return render(request, 'voitureEdit.html', {'form': form, 'voiture': voiture})

@login_required
def addVoiture(request):
    ImageFormSet = forms.modelformset_factory(ImageVoiture, form=ImageVoitureForm, extra=9)  # Permet d'ajouter jusqu'à 3 images
    if request.method == 'POST':
        voiture_form = VoitureForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ImageVoiture.objects.none())
        if voiture_form.is_valid() and formset.is_valid():
            voiture = voiture_form.save()
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    ImageVoiture.objects.create(voiture=voiture, image=image)
            return redirect('dashboard')  # Remplacez par le nom de l'URL de redirection
    else:
        voiture_form = VoitureForm()
        formset = ImageFormSet(queryset=ImageVoiture.objects.none())
    
    return render(request, 'addVoiture.html', {'voiture_form': voiture_form, 'formset': formset})


import stripe 
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View


stripe.api_key = settings.STRIPE_SECRET_KEY


    


############################### to here ############################### 

def checkout(request, voiture_id):
    voitureDetail=models.Voiture.objects.get(id=voiture_id)
    return render(request, 'checkout.html', {'voiture':voitureDetail})

class CheckoutSessionRest(View):
    def get(self, request, *args, **kwargs):
        vente_id = kwargs.get('vente_id')
        vente = models.Vente.objects.get(id=vente_id)

        marque = vente.voiture_id.marque if vente.voiture_id else 'Service'
        amount_type = request.GET.get('type', 'reste')  
        YOUR_DOMAIN = 'http://127.0.0.1:8000'

        amount_to_pay = 0  # Initialiser amount_to_pay

        if amount_type == 'acompte':
            if vente.montant_acompte:
                amount_to_pay = vente.montant_acompte
            else:
                amount_to_pay = vente.montant_total  # Assurez-vous de gérer ce cas

        else:  # Si amount_type n'est pas 'acompte'
            amount_to_pay = vente.montant_restant

        # Créez la session Stripe pour les deux cas
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': marque,
                    },
                    'unit_amount': int(amount_to_pay * 100),  # Stripe attends le montant en cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + ('/pay_success_accompte' if amount_type == 'acompte' else '/pay_success'),
            cancel_url=YOUR_DOMAIN + '/cancel',
        )

        # Stockez l'ID de la vente dans la session
        request.session['vente_id'] = vente_id

        return redirect(session.url, code=303)

def pay_success(request):
    vente_id = request.session.get('vente_id')  
    vente = Vente.objects.get(id=vente_id)

    vente.paid = 'yes'
    vente.voiture_id.status = 'vendu'

    vente.save()
    vente.voiture_id.save()
    messages.success(request, 'Paiement effectué avec succès !') 

    return redirect(reverse('profile_view', kwargs={'username': request.user.username}))

def pay_success_accompte(request):
    vente_id = request.session.get('vente_id')  
    vente = Vente.objects.get(id=vente_id)

    vente.paid = 'yes'
    if vente.voiture_id:
        vente.voiture_id.status = 'reservé'
        vente.paid = 'partially'
        vente.voiture_id.save()
    vente.save()
    messages.success(request, 'Paiement effectué avec succès !') 
    

    return redirect(reverse('profile_view', kwargs={'username': request.user.username}))



def car_delivery(request, voiture_id, demande_id):
    voiture = get_object_or_404(Voiture, pk=voiture_id)
    voiture.status = 'livré'
    voiture.save()

    demande = get_object_or_404(Demande, pk = demande_id)
    demande.status = 'Close'
    demande.save()
    return redirect('dashboard')

def car_deliveryDirect(request, voiture_id):
    voiture = get_object_or_404(Voiture, pk=voiture_id)
    voiture.status = 'livré'
    voiture.save()

    return redirect('dashboard')



def toggleFavoriteCar(request, voiture_id):
    voiture = get_object_or_404(Voiture, pk=voiture_id)
    wishlist, created = UserWishlist.objects.get_or_create(user=request.user)

    if wishlist.voiture.filter(pk=voiture_id).exists():
        wishlist.voiture.remove(voiture)
    else:
        wishlist.voiture.add(voiture)

    # Rediriger vers la page précédente
    return redirect(request.META.get('HTTP_REFERER', '/'))

from datetime import datetime
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


from datetime import datetime
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

def vente_facture_pdf(request, vente_id):
    # Récupérer la vente
    vente = get_object_or_404(Vente, id=vente_id)
    user = request.user
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 8

    # Configuration de la réponse HTTP pour un fichier PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{vente.voiture_id.marque}.pdf"'

    # Création du PDF avec ReportLab
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Informations de l'entreprise
    p.setFont("Helvetica", 10)
    entreprise_info = [
        "Cars - Services",
        "Adresse : 123, Rue des Voitures",
        "Ville : Bruxelles, BE 1020",
        "Tél. : +32 489 45 44 32",
        "Email : info@Cars-Service@gmail.com",
        "Horaires : Du Lu au Dim de 07h à 19h",
    ]
    for idx, line in enumerate(entreprise_info):
        p.drawString(width - 200, height - 50 - (15 * idx), line)

    # Informations sur l'utilisateur
    p.setFont("Helvetica", 10)
    user_info = [
        "Adresse de livraison",
        f"Nom: {user.first_name} {user.last_name}",
        f"Email: {user.email}",
        f"Tel: {getattr(user, 'phone', 'Non renseigné')}",
        f"Adresse: {getattr(user, 'address', 'Non renseignée')}",
    ]
    for idx, line in enumerate(user_info):
        p.drawString(50, height - 50 - (15 * idx), line)

    # Détails de la facture
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 145, f"Date de la facture : {datetime.now().strftime('%d/%m/%Y')}")
    p.drawString(50, height - 160, f"Numéro de facture : {vente.id}-{datetime.now().strftime('%Y%m%d')}")

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 200, "Facture d'achat")

    # Totaux
    y_position = height - 225
    price_tvac = Decimal(vente.montant_total)
    price_htva = price_tvac / Decimal("1.21")
    tva_amount = price_tvac - price_htva

    p.setFont("Helvetica", 12)
    voiture_details = [
        f"Marque du véhicule : {vente.voiture_id.marque}",
        f"Modèle du véhicule : {vente.voiture_id.modele}",
        f"Année du véhicule : {vente.voiture_id.annee_fabrication}",
        f"Numéro de chassis : {vente.voiture_id.num_chassis}",
        f"Total HTVA : {price_htva.quantize(Decimal('0.01'))}€",
        f"Total TVA (21%) : {tva_amount.quantize(Decimal('0.01'))}€",
        f"Total TVAC : {price_tvac.quantize(Decimal('0.01'))}€",
    ]
    for line in voiture_details:
        p.drawString(50, y_position, line)
        y_position -= 15

    # Clauses légales
    clauses = [
        ("Politique de rétractation :", "Conformément à la législation en vigueur, le droit de rétractation de 14 jours ne s'applique pas aux contrats de vente de véhicules d'occasion conclus à distance ou hors établissement. La vente est donc considérée comme définitive dès la signature du bon de commande ou du contrat de vente."),
        ("Garantie légale :", "Tous nos véhicules d'occasion sont couverts par la garantie légale de conformité de 2 ans, conformément aux articles L.217-4 et suivants du Code de la consommation. Cette garantie couvre les défauts de conformité existants au moment de la délivrance du véhicule et qui se manifestent dans un délai de 2 ans à compter de celle-ci. Sont exclus de la garantie légale les défauts résultant d'une usure normale du véhicule, d'un mauvais entretien ou d'une utilisation non conforme."),
        ("Confidentialité :", "Les informations recueillies lors de votre achat sont utilisées pour le traitement de votre commande et la gestion de notre relation client. Elles peuvent également être utilisées à des fins statistiques ou pour vous informer de nos offres commerciales. Conformément à la loi \"Informatique et Libertés\" du 6 janvier 1978 modifiée, vous disposez d'un droit d'accès, de rectification et de suppression des données vous concernant."),
    ]

    for title, text in clauses:
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y_position, title)
        y_position -= 15
        paragraph = Paragraph(text, style)
        w, h = paragraph.wrap(500, 100)  # Ajustement dynamique
        paragraph.drawOn(p, 50, y_position - h)
        y_position -= h + 20

    # Finalisation du PDF
    p.showPage()
    p.save()

    return response

def recu_accomte_pdf(request, vente_id):
    # Récupérer la vente
    vente = get_object_or_404(Vente, id=vente_id)
    user = request.user
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 8

    # Configuration de la réponse HTTP pour un fichier PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Recu_accompte_{vente.voiture_id.marque}_{vente.voiture_id.modele}_{vente.voiture_id.annee_fabrication}.pdf"'

    # Création du PDF avec ReportLab
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Informations de l'entreprise
    p.setFont("Helvetica", 10)
    entreprise_info = [
        "Cars - Services",
        "Adresse : 123, Rue des Voitures",
        "Ville : Bruxelles, BE 1020",
        "Tél. : +32 489 45 44 32",
        "Email : info@Cars-Service@gmail.com",
        "Horaires : Du Lu au Dim de 07h à 19h",
    ]
    for idx, line in enumerate(entreprise_info):
        p.drawString(width - 200, height - 50 - (15 * idx), line)

    # Informations sur l'utilisateur
    p.setFont("Helvetica", 10)
    user_info = [
        "Adresse de livraison",
        f"Nom: {user.first_name} {user.last_name}",
        f"Email: {user.email}",
        f"Tel: {getattr(user, 'phone', 'Non renseigné')}",
        f"Adresse: {getattr(user, 'address', 'Non renseignée')}",
    ]
    for idx, line in enumerate(user_info):
        p.drawString(50, height - 50 - (15 * idx), line)

    # Détails de la facture
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 145, f"Date d'émmission' : {datetime.now().strftime('%d/%m/%Y')}")
    p.drawString(50, height - 160, f"Numéro de transaction : {vente.id}-{datetime.now().strftime('%Y%m%d')}")

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 200, "Reçu d'accomte")

    # Totaux
    y_position = height - 225
    price_tvac = Decimal(vente.montant_total)
    price_htva = price_tvac / Decimal("1.21")
    tva_amount = price_tvac - price_htva
    total_accomte = Decimal(vente.montant_acompte)
    accomte_htva = Decimal(vente.montant_acompte / Decimal("1.21") )
    accomte_tva = total_accomte - accomte_htva
    
    p.setFont("Helvetica", 12)
    voiture_details = [
        f"Marque du véhicule : {vente.voiture_id.marque}",
        f"Modèle du véhicule : {vente.voiture_id.modele}",
        f"Année du véhicule : {vente.voiture_id.annee_fabrication}",
        f"Numéro de chassis : {vente.voiture_id.num_chassis}",
        f"Total HTVA : {price_htva.quantize(Decimal('0.01'))}€",
        f"Total TVA (21%) : {tva_amount.quantize(Decimal('0.01'))}€",
        f"Total TVAC : {price_tvac.quantize(Decimal('0.01'))}€",
        f"Montant de l'accomte reçu : {total_accomte.quantize(Decimal('0.01'))}€ dont {accomte_tva.quantize(Decimal('0.01'))}€ de tva",
    ]
    for line in voiture_details:
        p.drawString(50, y_position, line)
        y_position -= 15

    # Clauses légales
    clauses = [
        ("Politique de rétractation :", "Conformément à la législation en vigueur, le droit de rétractation de 14 jours ne s'applique pas aux contrats de vente de véhicules d'occasion conclus à distance ou hors établissement. La vente est donc considérée comme définitive dès la signature du bon de commande ou du contrat de vente."),
        ("Garantie légale :", "Tous nos véhicules d'occasion sont couverts par la garantie légale de conformité de 2 ans, conformément aux articles L.217-4 et suivants du Code de la consommation. Cette garantie couvre les défauts de conformité existants au moment de la délivrance du véhicule et qui se manifestent dans un délai de 2 ans à compter de celle-ci. Sont exclus de la garantie légale les défauts résultant d'une usure normale du véhicule, d'un mauvais entretien ou d'une utilisation non conforme."),
        ("Confidentialité :", "Les informations recueillies lors de votre achat sont utilisées pour le traitement de votre commande et la gestion de notre relation client. Elles peuvent également être utilisées à des fins statistiques ou pour vous informer de nos offres commerciales. Conformément à la loi \"Informatique et Libertés\" du 6 janvier 1978 modifiée, vous disposez d'un droit d'accès, de rectification et de suppression des données vous concernant."),
    ]
    y_position -= 50
    for title, text in clauses:
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y_position, title)
        y_position -= 15
        paragraph = Paragraph(text, style)
        w, h = paragraph.wrap(500, 100)  # Ajustement dynamique
        paragraph.drawOn(p, 50, y_position - h)
        y_position -= h + 20

    # Finalisation du PDF
    p.showPage()
    p.save()

    return response


def service_list(request):
    services = Service.objects.filter(is_available=True)
    review_form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user_id = request.user  # Assurez-vous que `request.user` est bien un `Member`
            review.service_id = get_object_or_404(Service, id=request.POST.get('service_id'))
            review.save()
            return redirect('service_list')

    return render(request, 'service_list.html', {
        'services': services,
        'review_form': review_form,
    })



