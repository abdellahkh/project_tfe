from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Marque, Modele, Voiture, Service, Review, Vente, Member, Demande, VoitureSoumisse

admin.site.register(Member)
admin.site.register(Marque)
#admin.site.register(Modele)
admin.site.register(Service)
admin.site.register(Review)


@admin.register(Modele)
class modeleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nom', 'marque')  # Ajoutez tous les champs que vous souhaitez afficher dans la liste
    list_filter = ('marque',)


@admin.register(Demande)
class DemandeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('service', 'status', 'member', 'date_desiree')  # Ajoutez tous les champs que vous souhaitez afficher dans la liste
    list_filter = ('status',)



@admin.register(Voiture)
class VoitureAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('reserve','sold', 'marque', 'modele', 'annee_fabrication', 'carburant')
    list_filter = ('reserve', 'sold')


@admin.register(Vente)
class VenteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('paid','user_id', 'demande_id', 'voiture_id', 'date', 'montant_total', 'montant_acompte')
    

@admin.register(VoitureSoumisse)
class VenteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('date_poste','user_id', 'first_name', 'last_name', 'email', 'phone', 'marque', 'modele', 'annee_fabrication', 'carburant', 'transmission', 'kilometrage', 'description', 'prix')
