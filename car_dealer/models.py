from django.db import models

class Marque(models.Model):
    nom = models.CharField(max_length=100, unique=True, help_text="Nom de la marque")

    def __str__(self):
        return self.nom

class Modele(models.Model):
    nom = models.CharField(max_length=100, help_text="Nom du modèle")
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, help_text="Marque à laquelle le modèle appartient")

    def __str__(self):
        return f"{self.nom}"

       
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
        ('Manuelle','Manuelle'),
        ('Automatique','Automatique'),
        ('Semi-automatique','Semi-qutomatique')
    ]
    
    reserve = models.BooleanField(default=False, verbose_name="Reserver")
    sold = models.BooleanField(default=False, verbose_name="Vendu")
    marque = models.ForeignKey(Marque, on_delete=models.PROTECT, related_name='voitures', help_text="Marque de la voiture")
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, help_text="Modèle de la voiture")
    annee_fabrication = models.PositiveIntegerField(help_text="Année de fabrication")
    carburant = carburant = models.CharField(
        null = True,
        blank = True,
        max_length=90,
        choices=CARBURANT_CHOICES,
        help_text="Type de carburant de la voiture"
    )
    transmission = models.CharField(
        null = True,
        blank = True,
        max_length=90,
        choices=TRANSMISSION_CHOICES,
        help_text="Type de transmission"
    )
    kilometrage = models.PositiveIntegerField(help_text="Kilométrage actuel")
    cruise_control = models.BooleanField(default=False, verbose_name="Cruise Control")
    direction_assistee = models.BooleanField(default=False, verbose_name="Direction assistée")
    audio_interface = models.BooleanField(default=False, verbose_name="Audio Interface")
    airbags = models.BooleanField(default=False, verbose_name="Airbags")
    air_conditionne = models.BooleanField(default=False, verbose_name="Air Conditioninne")
    siege_chauffant = models.BooleanField(default=False, verbose_name="Siege Chauffant")
    alarm_system = models.BooleanField(default=False, verbose_name="Alarm System")
    parkassist = models.BooleanField(default=False, verbose_name="Park Assist")
    camera_recul = models.BooleanField(default=False, verbose_name="Camera de Recul")
    start_stop = models.BooleanField(default=False, verbose_name="Start Stop")
    essui_auto = models.BooleanField(default=False, verbose_name="Essui-glace Auto")
    car_play = models.BooleanField(default=False, verbose_name="Car Play-System")
    
    
    description = models.TextField(blank=True, null=True, help_text="Description de la voiture")
    date_poste = models.DateTimeField(auto_now_add=True, help_text="Date de publication de l'annonce")
    #photos_1 = models.ImageField(upload_to='images/voitures/', blank=True, null=True, help_text="Image de la voiture")


    
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
        ordering = ['-date_poste']  # Tri par date de publication par défaut

    def __str__(self):
        return f"({self.marque}) {self.modele} - {self.annee_fabrication}"


