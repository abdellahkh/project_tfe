from django.db import models
from django.contrib.auth.models import User, AbstractUser



class Member(AbstractUser):
    STATUS = (
        ('normal', 'normal'),
        ('client', 'client'),
        ('vendeur', 'vendeur')
    )
    status = models.CharField(max_length=100, choices=STATUS, default='normal')
    username = models.CharField(max_length=100, unique=True, help_text="username")
    first_name = models.CharField(max_length=100, help_text="Prenom")
    last_name = models.CharField(max_length=100, help_text="Nom")
    email = models.EmailField(max_length=100, help_text="Email")
    phone = models.CharField(max_length=100, help_text="Phone", blank=True, null=True)
    address = models.CharField(max_length=100, help_text="adresse", blank=True, null=True)
    postal = models.IntegerField(null=True, blank=True, help_text="Code Postal")
    ville = models.CharField(max_length=100, help_text="Ville", blank=True, null=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class Marque(models.Model):
    nom = models.CharField(max_length=100, unique=True, help_text="Nom de la marque")

    def __str__(self):
        return self.nom

class Modele(models.Model):
    nom = models.CharField(max_length=100, help_text="Nom du modèle")
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, help_text="Marque à laquelle le modèle appartient")

    def __str__(self):
        return self.nom

class Voiture(models.Model):
    CARBURANT_CHOICES = [
        ('Diesel', 'Diesel'),
        ('Essence', 'Essence'),
        ('Ethanol', 'Ethanol'),
        ('Electrique', 'Electrique'),
        ('Hydrogene', 'Hydrogene'),
        ('LPG', 'LPG'),
        ('CNG', 'CNG'),
        ('Hybride (Elec - Ess)', 'Hybride (Elec - Ess)'),
        ('Hybride (Elec - Diesel)', 'Hybride (Elec - Diesel)'),
        ('Autres', 'Autres'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('Manuelle', 'Manuelle'),
        ('Automatique', 'Automatique'),
        ('Semi-automatique', 'Semi-automatique'),
    ]
    
    STATUS_CHOICES = [
        ('standby', 'Standby'),
        ('avendre' ,'A vendre'),
        ('reservé', 'Reservé'),
        ('transit' ,'transit'),
        ('vendu', 'Vendu'),
    ]
    
    

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='standby',
        help_text="Statut de la voiture"
    )
    
    marque = models.ForeignKey(Marque, on_delete=models.PROTECT, related_name='voitures', help_text="Marque de la voiture")
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, help_text="Modèle de la voiture")
    annee_fabrication = models.PositiveIntegerField(help_text="Année de fabrication")
    carburant = models.CharField(
        null=True,
        blank=True,
        max_length=90,
        choices=CARBURANT_CHOICES,
        help_text="Type de carburant de la voiture"
    )
    transmission = models.CharField(
        null=True,
        blank=True,
        max_length=90,
        choices=TRANSMISSION_CHOICES,
        help_text="Type de transmission"
    )
    kilometrage = models.PositiveIntegerField(help_text="Kilométrage actuel")

    cruise_control = models.BooleanField(default=False, help_text="Contrôle de croisière")
    direction_assistee = models.BooleanField(default=False, help_text="Direction assistée")
    audio_interface = models.BooleanField(default=False, help_text="Interface audio")
    airbags = models.BooleanField(default=False, help_text="Airbags")
    air_conditionne = models.BooleanField(default=False, help_text="Climatisation")
    siege_chauffant = models.BooleanField(default=False, help_text="Sièges chauffants")
    alarm_system = models.BooleanField(default=False, help_text="Système d'alarme")
    parkassist = models.BooleanField(default=False, help_text="Aide au stationnement")
    camera_recul = models.BooleanField(default=False, help_text="Caméra de recul")
    start_stop = models.BooleanField(default=False, help_text="Système start/stop")
    essui_auto = models.BooleanField(default=False, help_text="Essuie-glace automatique")
    car_play = models.BooleanField(default=False, help_text="Apple CarPlay")
    
    description = models.TextField(blank=True, null=True, help_text="Description de la voiture")
    date_poste = models.DateTimeField(auto_now_add=True, help_text="Date de publication de l'annonce")

    prix = models.DecimalField(max_digits=10, decimal_places=0, help_text="Prix de la voiture")
    prix_min = models.DecimalField(max_digits=10, decimal_places=0, help_text="Prix minimale de vente")

    class Meta:
        ordering = ['-date_poste']

    def __str__(self):
        return f"{self.marque} {self.modele} - {self.annee_fabrication}"
    
class ImageVoiture(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    
    def __str__(self):
        return f"Image de {self.voiture}"



class Option(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

    
class VoitureSoumisse(models.Model):
    CARBURANT_CHOICES = [
        ('Diesel', 'Diesel'),
        ('Essence', 'Essence'),
        ('Ethanol', 'Ethanol'),
        ('Electrique', 'Electrique'),
        ('Hydrogene', 'Hydrogene'),
        ('LPG', 'LPG'),
        ('CNG', 'CNG'),
        ('Hybride (Elec - Ess)', 'Hybride (Elec - Ess)'),
        ('Hybride (Elec - Diesel)', 'Hybride (Elec - Diesel)'),
        ('Autres', 'Autres'),
    ]
    TRANSMISSION_CHOICES = [
        ('Manuelle', 'Manuelle'),
        ('Automatique', 'Automatique'),
        ('Semi-automatique', 'Semi-automatique'),
    ]
    user_id = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True, help_text="Identifiant du membre qui a soumis la voiture")
    first_name = models.CharField(blank=True, null=True,max_length=100, help_text="Prenom")
    last_name = models.CharField(blank=True, null=True,max_length=100, help_text="Nom")
    email = models.EmailField(blank=True, null=True,max_length=100, help_text="Email")
    phone = models.CharField(max_length=100, help_text="Phone", blank=True, null=True)
    marque = models.CharField(max_length=100, help_text="Marque", blank=True, null=True)
    modele = models.CharField(max_length=100, help_text="Modele", blank=True, null=True)
    annee_fabrication = models.PositiveIntegerField(help_text="Année de fabrication")
    carburant = models.CharField(
        null=True,
        blank=True,
        max_length=90,
        choices=CARBURANT_CHOICES,
        help_text="Type de carburant de la voiture"
    )
    transmission = models.CharField(
        null=True,
        blank=True,
        max_length=90,
        choices=TRANSMISSION_CHOICES,
        help_text="Type de transmission"
    )
    kilometrage = models.PositiveIntegerField(help_text="Kilométrage actuel")
    cruise_control = models.BooleanField(default=False, verbose_name="Cruise Control")
    direction_assistee = models.BooleanField(default=False, verbose_name="Direction assistée")
    audio_interface = models.BooleanField(default=False, verbose_name="Audio Interface")
    airbags = models.BooleanField(default=False, verbose_name="Airbags")
    air_conditionne = models.BooleanField(default=False, verbose_name="Air Conditionné")
    siege_chauffant = models.BooleanField(default=False, verbose_name="Siège Chauffant")
    alarm_system = models.BooleanField(default=False, verbose_name="Alarm System")
    parkassist = models.BooleanField(default=False, verbose_name="Park Assist")
    camera_recul = models.BooleanField(default=False, verbose_name="Camera de Recul")
    start_stop = models.BooleanField(default=False, verbose_name="Start Stop")
    essui_auto = models.BooleanField(default=False, verbose_name="Essuie-glace Auto")
    car_play = models.BooleanField(default=False, verbose_name="Car Play-System")
    
    description = models.TextField(blank=True, null=True, help_text="Description de la voiture")
    date_poste = models.DateField(auto_now_add=True, help_text="Date de publication de l'annonce")

    car_photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo_7 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo_8 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo_9 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    prix = models.DecimalField(max_digits=10, decimal_places=0, help_text="Prix de la voiture")

    class Meta:
        ordering = ['-date_poste']

    def __str__(self):
        return f"{self.marque} {self.modele} - {self.annee_fabrication}"

class Service(models.Model):
    is_available = models.BooleanField(default=False, verbose_name="Disponible")
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    nom = models.CharField(max_length=100, help_text="Nom du service")
    description = models.TextField(blank=True, null=True, help_text="Commentaire")
    prix = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True,help_text="Prix du service")

    def __str__(self):
        return self.nom

class Review(models.Model):
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE, help_text="Identifiant du membre qui a commenté")
    comment = models.TextField(blank=True, null=True, help_text="Commentaire")
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, help_text="Identifiant du Service")

    def __str__(self):
        return f"({self.user_id.username}) : {self.comment}"

class Demande(models.Model):
    GENRE_INTERVENTION = [
        ('Entretien', 'Entretien'),
        ('Reparation, panne', 'Reparation, panne'),
        ('Carrosserie', 'Carrosserie'),
        ('Deplacement', 'Deplacement'),
        ('Info', 'Info'),
    ]
    STATUS_OPTIONS = [
        ('Actif', 'Actif'),
        ('En preparation', 'En preparation'),
        ('Close', 'Close'),
    ]
    status = models.CharField(
        null=True,
        blank=True,
        max_length=90,
        choices=STATUS_OPTIONS,
        help_text="Type de service",
        default='Actif'
    )
    member = models.ForeignKey(Member, on_delete=models.CASCADE,blank=True, null=True, help_text="Service selectionner")
    first_name = models.CharField(max_length=100,blank=True, null=True, help_text="Prenom")
    last_name = models.CharField(max_length=100, blank=True, null=True, help_text="Nom")
    email = models.EmailField(max_length=100,blank=True, null=True, help_text="Email")
    phone = models.CharField(max_length=100, help_text="Phone", blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, help_text="Service selectionner")
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE, blank=True, null=True, help_text="Email")
    date = models.DateTimeField(auto_now_add=True, help_text="Date de la demande")
    date_desiree = models.DateField(auto_now_add=False, blank=True, null=True, help_text="  (Date d'intervention souhaitée)")
    details = models.TextField(blank=True, null=True, help_text="Details specifique")
    genre = models.CharField(
        null=True,
        blank=True,
        max_length=90,
        choices=GENRE_INTERVENTION,
        help_text="Type de service"
    )
    startLocation = models.CharField(max_length=100, help_text="Commune depart", blank=True, null=True)
    endLocation = models.CharField(max_length=100, help_text="Commune arrivee", blank=True, null=True)
    car_doc = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        if self.member:
            return f"{self.service} - {self.member}: {self.date_desiree}"
        else:
            return f"{self.service} - {self.first_name}, {self.last_name}: {self.date_desiree}"

class Vente(models.Model):
    GENRE_CHOICES = [
        ('Vente', 'Vente'),
        ('Service', 'Service'),
    ]
    genre = models.CharField(
        null=True,
        blank=True,
        max_length=90,
        choices=GENRE_CHOICES,
        help_text="Type de service"
    )
    paid = models.BooleanField(default=False, verbose_name="Payé") 
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE, help_text="Identifiant du User")
    demande_id = models.ForeignKey(Demande, blank=True, null=True, on_delete=models.CASCADE, help_text="Identifiant du Service")
    voiture_id = models.ForeignKey(Voiture, blank=True, null=True,  on_delete=models.CASCADE, help_text="Identifiant de la voiture")
    date = models.DateTimeField(auto_now_add=True, help_text="Date de la vente")
    montant_total = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, help_text="Montant total de la vente")
    montant_acompte = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, help_text="Montant de l'acompte")