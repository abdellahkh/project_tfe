from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Marque, Modele, Voiture, Service, Review, Vente, Member, Demande

admin.site.register(Member)
admin.site.register(Marque)
admin.site.register(Modele)
admin.site.register(Service)
admin.site.register(Review)
admin.site.register(Demande)
admin.site.register(Vente)

@admin.register(Voiture)
class VoitureAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('reserve','sold', 'marque', 'modele', 'annee_fabrication', 'carburant')