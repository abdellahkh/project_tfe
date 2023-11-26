from django.shortcuts import render, redirect
from .models import Service, Voiture, Member, Demande
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserUpdateForm, DemandeDeplacement
from django import forms
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model


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
        messages.success(request, f'Cher {user}, verifie votre boite de messagerie <b>{to_email}</b> et cliquez sur \
                        le lien d\'activation pour confirmer l\'inscription.')
    else:
        messages.error(request, f'Une erreur est survenue. Verifie l\'adresse: {to_email}.')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
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
    services = Service.objects.all()
    return render(request, 'allServices.html', { 'services': services })

def voiture(request, pk):
    voiture = Voiture.objects.get(id=pk)
    return render(request, 'voiture.html' ,{'voiture' : voiture})



from django.shortcuts import render, redirect
from .models import Service
from .forms import DemandeDeplacement  # Make sure to import your form

def service(request, service_id):
    submitted = False
    service = Service.objects.get(id=service_id)

    if service.nom == 'Déplacement de Véhicule Longue Distance' or service.nom == 'Déplacement de Véhicule Courte Distance':
        if request.method == 'POST':
            form = DemandeDeplacement(request.POST)
            form.instance.service = service
            if form.is_valid():
                form.save()
                messages.success(request, 'Votre demande a bien été soumise, vous allez être recontacté sous peu.')
                return redirect('home')
            else:
                # Affichez le formulaire et les erreurs sur la console
                print(form.errors)
                messages.error(request, 'Hmm une erreur s\'est produite, veuillez réessayer plus tard')
        else:
            form = DemandeDeplacement()  # Corrected this line
            if 'submitted' in request.GET:
                submitted = True
    else:
        form = None

    return render(request, 'formulaire/service_demande.html', {'form': form, 'submitted': submitted, 'service': service})

def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)  # Utilisez le même nom 'form' ici
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'{user_form.username}, Votre profil a bien été modifié')
            return redirect("profile", user_form.username)
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
    return render(request, 'formulaire/vendre.html', {})