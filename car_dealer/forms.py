from .models import Member, VoitureSoumisse
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Member, Demande
from django.contrib.auth import get_user_model
from django.forms import ModelForm



class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="", 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adresse Email'})
    )
    first_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Prénom'})
    )
    last_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nom'})
    )
    address = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adresse (Rue et Numéro)'})
    )
    postal = forms.IntegerField(
        label="", 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Code Postal'})
    )
    ville = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ville'})
    )
    phone = forms.CharField(
        label="", 
        max_length=15,  # Changement en string pour plus de flexibilité
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Téléphone'}),
        required=False
    )

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'address', 'postal', 'ville', 'password1', 'password2')
    def clean_postal_code(self):
        postal = self.cleaned_data.get('postal')
        try:
            postal = int(postal)  # Convertir en entier
        except (ValueError, TypeError):
            raise forms.ValidationError("Veuillez entrer un code postal valide.")
        return postal

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs['class'] = 'form-control'
            self.fields[fieldname].label = ''
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['placeholder'] = fieldname.capitalize()


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
        fields = ['date_desiree', 'startLocation', 'endLocation', 'details']
        widgets = {
            'date_desiree': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'true'}),
            'startLocation': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'endLocation': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'required': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        super(DemandeDeplacementMembre, self).__init__(*args, **kwargs)
        self.fields['date_desiree'].label = 'Date'

		
class DemandeContactVoitureMembre(forms.ModelForm):

    class Meta:
        model = Demande
        fields = ['first_name', 'last_name', 'email', 'phone', 'details']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(DemandeContactVoitureMembre, self).__init__(*args, **kwargs)

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
    class Meta:
        model = VoitureSoumisse
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'marque',
            'modele',
            'annee_fabrication',
            'carburant',
            'transmission',
            'kilometrage',
            'cruise_control',
            'direction_assistee',
            'audio_interface',
            'airbags',
            'air_conditionne',
            'siege_chauffant',
            'alarm_system',
            'parkassist',
            'camera_recul',
            'start_stop',
            'essui_auto',
            'car_play',
            'description',
            'car_photo_1',
            'car_photo_2',
            'car_photo_3',
            'car_photo_4',
            'car_photo_5',
            'car_photo_6',
            'car_photo_7',
            'car_photo_8',
            'car_photo_9',
            'prix',
            'car_doc',
        ]

    
    car_doc = forms.ImageField()
    details = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(VenteVehicule, self).__init__(*args, **kwargs)
        for field_name in ['first_name', 'last_name', 'email', 'phone', 'marque', 'modele', 'annee_fabrication', 'carburant', 'transmission']:
            self.fields[field_name].required = True
        self.fields['car_doc'].required = False

class VenteVehiculeMembre(forms.ModelForm):
    class Meta:
        model = VoitureSoumisse
        fields = [
            'marque',
            'modele',
            'annee_fabrication',
            'carburant',
            'transmission',
            'kilometrage',
            'cruise_control',
            'direction_assistee',
            'audio_interface',
            'airbags',
            'air_conditionne',
            'siege_chauffant',
            'alarm_system',
            'parkassist',
            'camera_recul',
            'start_stop',
            'essui_auto',
            'car_play',
            'description',
            'car_photo_1',
            'car_photo_2',
            'car_photo_3',
            'car_photo_4',
            'car_photo_5',
            'car_photo_6',
            'car_photo_7',
            'car_photo_8',
            'car_photo_9',
            'prix',
            'car_doc',
        ]

    
    car_doc = forms.ImageField()
    details = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(VenteVehiculeMembre, self).__init__(*args, **kwargs)
        for field_name in ['marque', 'modele', 'annee_fabrication', 'carburant', 'transmission']:
            self.fields[field_name].required = True
        self.fields['car_doc'].required = False