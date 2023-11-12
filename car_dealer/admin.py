from django.contrib import admin

from .models import Marque, Modele, Voiture

admin.site.register(Marque)
admin.site.register(Modele)
admin.site.register(Voiture)