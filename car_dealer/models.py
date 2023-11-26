from django.db import models
from django.contrib.auth.models import User, AbstractUser



class Member(AbstractUser):
    STATUS = (
        ('normal', 'normal'),
        ('client', 'client')
    )
    status = models.CharField(max_length=100, choices=STATUS, default='normal')
    username = models.CharField(max_length=100, unique=True, help_text="username")
    first_name = models.CharField(max_length=100, help_text="Prenom")
    last_name = models.CharField(max_length=100, help_text="Nom")
    email = models.EmailField(max_length=100, help_text="Nom du modèle")
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
    
    reserve = models.BooleanField(default=False, verbose_name="Réserver")
    sold = models.BooleanField(default=False, verbose_name="Vendu")
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
    date_poste = models.DateTimeField(auto_now_add=True, help_text="Date de publication de l'annonce")

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
    
    reserve = models.BooleanField(default=False, verbose_name="Réserver")
    sold = models.BooleanField(default=False, verbose_name="Vendu")
    marque = models.ForeignKey(Marque, on_delete=models.PROTECT, related_name='voitures_a_lachat', help_text="Marque de la voiture")
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
    date_poste = models.DateTimeField(auto_now_add=True, help_text="Date de publication de l'annonce")

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
    service_id = models.ForeignKey(Service, blank=True, null=True, on_delete=models.CASCADE, help_text="Identifiant du Service")
    voiture_id = models.ForeignKey(Voiture, blank=True, null=True,  on_delete=models.CASCADE, help_text="Identifiant de la voiture")
    date = models.DateTimeField(auto_now_add=True, help_text="Date de la vente")
    montant_total = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, help_text="Montant total de la vente")
    montant_acompte = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, help_text="Montant de l'acompte")


class Demande(models.Model):
    GENRE_INTERVENTION = [
        ('Entretien', 'Entretien'),
        ('Reparation, panne', 'Reparation, panne'),
        ('Carrosserie', 'Carrosserie')
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, help_text="Service selectionner")
    date = models.DateTimeField(auto_now_add=True, help_text="Date de la demande")
    date_desiree = models.DateTimeField(auto_now_add=False, blank=True, null=True, help_text="  (Date d'intervention souhaitée)")
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

    def __str__(self):
        return f"{self.service} : {self.date_desiree}"

    

