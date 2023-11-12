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
    marque = models.ForeignKey(Marque, on_delete=models.PROTECT, related_name='voitures', help_text="Marque de la voiture")
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, help_text="Modèle de la voiture")
    annee_fabrication = models.PositiveIntegerField(help_text="Année de fabrication")
    kilometrage = models.PositiveIntegerField(help_text="Kilométrage actuel")
    prix = models.DecimalField(max_digits=10, decimal_places=2, help_text="Prix de la voiture")
    description = models.TextField(blank=True, null=True, help_text="Description de la voiture")
    date_poste = models.DateTimeField(auto_now_add=True, help_text="Date de publication de l'annonce")
    photos = models.ImageField(upload_to='images/voitures/', blank=True, null=True, help_text="Image de la voiture")

    class Meta:
        ordering = ['-date_poste']  # Tri par date de publication par défaut

    def __str__(self):
        return f"({self.marque}) {self.modele} - {self.annee_fabrication}"


class Photo(models.Model):
    image = models.ImageField(upload_to='images/voitures/', help_text="Image de la voiture")

    def __str__(self):
        return f"Photo {self.id}"
