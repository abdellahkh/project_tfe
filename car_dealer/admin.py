from django.contrib import admin

from .models import Marque, Modele, Voiture, Service, Review, Vente

admin.site.register(Marque)
admin.site.register(Modele)
admin.site.register(Voiture)
admin.site.register(Service)
admin.site.register(Review)
admin.site.register(Vente)