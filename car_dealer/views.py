from django.shortcuts import render, redirect
from .models import Service, Voiture, Member, Demande, VoitureSoumisse
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import DemandeContactVoitureMembre, SignUpForm, UserUpdateForm, DemandeDeplacement, DemandeControlTech, DemandeControlTechMembre, DemandeDeplacementMembre, DemandeSortieDeFourriereMembre, DemandeSortieDeFourriere, VenteVehicule, VenteVehiculeMembre
from django import forms
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

from car_dealer import models


# Create your views here.
def home(request):
    voitures = Voiture.objects.all()
    services = Service.objects.all()
    return render(request, 'home.html', {'voitures' :voitures, 'services' : services})

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

def dashboard(request):
    return render(request, 'dashboard/index.html', {})


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
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')
        else:
            messages.success(request, ("Ooops, une erreur s'est produite"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Print user info for debugging
        print(f"Tentative de connexion : Nom d'utilisateur : {username}, Mot de passe : {password}")
        
        if not username or not password:
            messages.error(request, "Les champs nom d'utilisateur et mot de passe sont obligatoires.")
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        
        # Print the result of the authentication
        if user is not None:
            print(f"Utilisateur trouvé : {user}")
            login(request, user)
            messages.success(request, "Vous êtes connecté.")
            return redirect('home')
        else:
            print("Aucun utilisateur trouvé avec ces identifiants.")
            messages.error(request, "Une erreur est survenue, veuillez réessayer.")
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
    return render(request, 'allServices.html', { 'services': services })

def voiture(request, pk):
    voiture = Voiture.objects.get(id=pk)
    return render(request, 'voiture.html' ,{'voiture' : voiture})


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
                    serviceEmailToAdminFromMembre(request, user, service_nom, form, mail_to, None)
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
                    serviceEmailToAdmin(request, user, service_nom, form, mail_to, None)
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
                    serviceEmailToAdminFromMembre(request, user, service_nom, form, mail_to, None)
                    return redirect('home')
                else:
                    print(form.errors)
                    messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
            else:
                form = DemandeControlTechMembre()
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
                    serviceEmailToAdmin(request, user, service_nom, form, mail_to, None)
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
                    serviceEmailToAdminFromMembre(request, user, service_nom, form, mail_to, None)
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
                    serviceEmailToAdmin(request, user, service_nom, form, mail_to, voiture)
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
                    serviceEmailToAdmin(request, user, service_nom, form, mail_to, voiture)
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
                    serviceEmailToAdmin(request, user, service_nom, form, mail_to, voiture)
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
                    serviceEmailToAdminFromMembre(request, user, service_nom, form, mail_to)
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
                    serviceEmailToAdmin(request, user, service_nom, form, mail_to)
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
    voiture = Voiture.objects.get(id = voiture_id)
    service_nom = 'Contact pour information voiture'
    mail_to = 'etu.abkh@gmail.com'
    service = Service.objects.get(id=9)
    if request.user.is_authenticated:
            if request.method == 'POST':
                form = DemandeContactVoitureMembre(request.POST)
                form.instance.member = request.user
                if form.is_valid():
                    form.save()
                    serviceEmailToAdminFromMembre(request, user, service_nom, form, mail_to)
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
                form.instance.member = request.user.id
                if form.is_valid():
                    user = {
                        'first_name': form.cleaned_data['first_name'],
                        'last_name': form.cleaned_data['last_name'],
                        'phone': form.cleaned_data['phone'],
                        'email': form.cleaned_data['email'],
                    }
                    form.save()
                    serviceEmailToAdmin(request, user, service_nom, form, mail_to)
                    return redirect('home')
                else:
                    print(form.errors)
                    messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
            else:
                form = DemandeContactVoitureMembre()
                if 'submitted' in request.GET:
                    submitted = True
    return render(request, 'formulaire/service_demande.html', {'voiture': voiture, 'service': service})


def profile(request, username):
    user = get_user_model().objects.filter(username=username).first()
    demandes = Demande.objects.filter(member=user)
    voitureSoumisses = VoitureSoumisse.objects.filter(user_id=user) 
    toutesDemandes = Demande.objects.all()
    toutesVoituresSoumise = VoitureSoumisse.objects.all()
    return render(request, "profile_view.html", {'user':user, 'demandes': demandes, 'voitureSoumisses':voitureSoumisses, 'toutesDemandes': toutesDemandes})




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
                serviceEmailToAdminFromMembre(request, user, service_nom, form, mail_to)
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
                serviceEmailToAdmin(request, user, service_nom, form, mail_to)
                return redirect('home')
            else:
                print(form.errors)
                messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
        else:
            form = VenteVehicule()
            if 'submitted' in request.GET:
                submitted = True
    return render(request, 'formulaire/vendre.html', {})


    




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

def checkout_session(request, voiture_id):
    mail_to = 'etu.abkh@gmail.com'
    user = request.user
    service_nom = "Vente"
    product = Voiture.objects.get(id=voiture_id)
    YOUR_DOMAIN = 'http://127.0.0.1:8002'
    montant_accomte = int(float(product.prix)*100*0.1)
    session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f"L'accomte à payer est de 10% du prix de la voiture {product.marque} {product.modele}\n\n{product.annee_fabrication}",
                        },
                        'unit_amount': montant_accomte,  
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/pay_success',
            cancel_url=YOUR_DOMAIN + '/pay_cancel',
            metadata={
                'voiture_id': str(product.id),
                'marque': product.marque,
                'modele': product.modele,
                'annee': str(product.annee_fabrication),
            },
        )
    montant_accomte = montant_accomte/100
    venteEmailToAdminFromMembre(request, user, service_nom, product, mail_to, montant_accomte)
    
    return redirect(session.url, code=303)


def pay_success(request):
    return render(request, 'success.html')

def pay_cancel(request):
    return render(request, 'cancel.html')