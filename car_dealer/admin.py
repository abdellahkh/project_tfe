from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html

from .models import Marque, Modele, Voiture, Service, Review, Vente, Member, Demande, VoitureSoumisse

admin.site.register(Member)
admin.site.register(Marque)
admin.site.register(Modele)
admin.site.register(Service)
admin.site.register(Review)
admin.site.register(Demande)

@admin.register(Voiture)
class VoitureAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'status',
        'marque',
        'modele',
        'annee_fabrication',
        'carburant',
        'transmission',
        'kilometrage',
        'prix',
        'prix_min',
        'date_poste',  # Affiché en mode liste
        'display_options'
    )

    def display_options(self, obj):
        """ Affiche les options booléennes sous forme de tableau. """
        options = {
            'Cruise Control': obj.cruise_control,
            'Direction Assistée': obj.direction_assistee,
            'Interface Audio': obj.audio_interface,
            'Airbags': obj.airbags,
            'Climatisation': obj.air_conditionne,
            'Sièges Chauffants': obj.siege_chauffant,
            'Système d\'Alarme': obj.alarm_system,
            'Aide au Stationnement': obj.parkassist,
            'Caméra de Recul': obj.camera_recul,
            'Système Start/Stop': obj.start_stop,
            'Essuie-glace Automatique': obj.essui_auto,
            'Apple CarPlay': obj.car_play,
        }
        
        html = '<ul>'
        for label, value in options.items():
            html += f'<li>{label}: {"Oui" if value else "Non"}</li>'
        html += '</ul>'
        
        return format_html(html)

    display_options.short_description = 'Options'

    fieldsets = (
        (None, {
            'fields': ('status', 'marque', 'modele', 'annee_fabrication', 'carburant', 'transmission', 'kilometrage', 'prix', 'prix_min')
        }),
        ('Options', {
            'fields': ('cruise_control', 'direction_assistee', 'audio_interface', 'airbags', 'air_conditionne', 'siege_chauffant', 'alarm_system', 'parkassist', 'camera_recul', 'start_stop', 'essui_auto', 'car_play'),
            'classes': ('collapse',),  # Permet de réduire la section options
        }),
        ('Images', {
            'fields': ('car_photo_1', 'car_photo_2', 'car_photo_3', 'car_photo_4', 'car_photo_5', 'car_photo_6', 'car_photo_7', 'car_photo_8', 'car_photo_9')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        # Ne pas inclure 'date_poste' ici car il est non éditable
    )
    
    readonly_fields = ('date_poste',) 


@admin.register(Vente)
class VenteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('paid','user_id', 'demande_id', 'voiture_id', 'date', 'montant_total', 'montant_acompte')
    

@admin.register(VoitureSoumisse)
class VenteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('date_poste','user_id', 'first_name', 'last_name', 'email', 'phone', 'marque', 'modele', 'annee_fabrication', 'carburant', 'transmission', 'kilometrage', 'description', 'prix')
