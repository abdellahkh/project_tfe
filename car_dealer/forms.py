from .models import Member, VoitureSoumisse
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Member, Demande
from django.contrib.auth import get_user_model
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Rue et numero'}))
	postal_code = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Code Postal'}))
	phone = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone', 'required': False}), required=False)

	class Meta:
		model = Member
		fields = ('username', 'first_name', 'last_name', 'email','phone' ,'address','postal_code', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'UserName'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small></small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'



class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = get_user_model()
		fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'postal', 'ville']
	

class DemandeDeplacement(forms.ModelForm):

    class Meta:
        model = Demande
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_desiree', 'startLocation', 'endLocation', 'details']
        widgets = {
            'date_desiree': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'startLocation': forms.TextInput(attrs={'class': 'form-control'}),
            'endLocation': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(DemandeDeplacement, self).__init__(*args, **kwargs)

        self.fields['date_desiree'].label = 'Date'

        # Set required for specific fields
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['date_desiree'].required = True
		

		
	
class DemandeDeplacementMembre(forms.ModelForm):

	class Meta:
		model = Demande
		fields = ['date_desiree', 'startLocation', 'endLocation', 'details',]
		widgets = {
            'date_desiree': forms.DateInput(attrs={'type': 'date'}),
        }

	def __init__(self, *args, **kwargs):
		super(DemandeDeplacementMembre, self).__init__(*args, **kwargs)

		self.fields['date_desiree'].label = 'Date'
		

class DemandeControlTechMembre(forms.ModelForm):

    class Meta:
        model = Demande
        fields = ['date_desiree', 'startLocation', 'endLocation', 'car_doc', 'details']
        widgets = {
            'date_desiree': forms.DateInput(attrs={'type': 'date'}),
            'car_doc': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super(DemandeControlTechMembre, self).__init__(*args, **kwargs)

class DemandeControlTech(forms.ModelForm):

    class Meta:
        model = Demande
        fields = ['first_name', 'last_name', 'phone', 'email', 'date_desiree', 'startLocation', 'car_doc', 'details']
        widgets = {
            'date_desiree': forms.DateInput(attrs={'type': 'date'}),
            'car_doc': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super(DemandeControlTech, self).__init__(*args, **kwargs)
		

class DemandeSortieDeFourriereMembre(forms.ModelForm):

	class Meta:
		model = Demande
		fields = ['date_desiree', 'startLocation', 'endLocation','car_doc' , 'details',]

	def __init__(self, *args, **kwargs):
		super(DemandeSortieDeFourriereMembre, self).__init__(*args, **kwargs)

		self.fields['date_desiree'].label = 'Date'

class DemandeSortieDeFourriere(forms.ModelForm):

	class Meta:
		model = Demande
		fields = ['first_name','last_name' ,'email','phone' ,'date_desiree', 'startLocation', 'endLocation','car_doc' , 'details',]

	def __init__(self, *args, **kwargs):
		super(DemandeSortieDeFourriere, self).__init__(*args, **kwargs)

		self.fields['date_desiree'].label = 'Date'


class VenteVehicule(forms.ModelForm):
    # Champs pour le modèle VoitureSoumisse
    marque = forms.CharField()
    modele = forms.CharField()
    annee_fabrication = forms.IntegerField()
    carburant = forms.CharField()
    transmission = forms.CharField()
    kilometrage = forms.IntegerField()
    description = forms.CharField()
    car_photo_1 = forms.ImageField()
    prix = forms.DecimalField()

    # Champs pour le modèle Demande
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    date_desiree = forms.DateField()
    startLocation = forms.CharField()
    endLocation = forms.CharField()
    car_doc = forms.ImageField()
    details = forms.CharField()

    class Meta:
        model = VoitureSoumisse
        fields = ['marque', 'modele', 'annee_fabrication', 'carburant', 'transmission', 'kilometrage', 'description', 'car_photo_1', 'prix']

    class Meta:
        model = Demande
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_desiree', 'startLocation', 'endLocation', 'car_doc', 'details']

    def __init__(self, *args, **kwargs):
        super(VenteVehicule, self).__init__(*args, **kwargs)
