from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html

from import_export import resources
from import_export.fields import Field
from .models import Modele, Marque, Notes, Voiture, ImageVoiture, Service, Review, Vente, Member, Demande, VoitureSoumisse

admin.site.register(Member)
admin.site.register(Review)

from .models import Voiture, ImageVoiture

class ImageVoitureInline(admin.TabularInline):
    model = ImageVoiture
    extra = 1  # Nombre d'images supplémentaires vides à afficher dans l'admin
    fields = ('image_tag', 'image')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="100" height="auto" />')
        return "-"
    image_tag.short_description = 'Aperçu'

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
        'date_poste',
        'display_options'
    )

    def display_options(self, obj):
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
            'classes': ('collapse',),
        }),
        # Supprimer la section "Images" ici
        ('Description', {
            'fields': ('description',)
        }),
    )

    readonly_fields = ('date_poste',)

    inlines = [ImageVoitureInline]


from django.utils.html import format_html

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'is_available', 'prix', 'description', 'image_tag')
    list_filter = ('is_available',)
    search_fields = ('nom',)
    
    fields = ('is_available', 'image', 'nom', 'description', 'prix')  # Champs du formulaire

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return None
    image_tag.short_description = 'Image'

admin.site.register(Service, ServiceAdmin)



class ImageVoitureInline(admin.TabularInline):
    model = ImageVoiture
    extra = 1
    fields = ['image', 'image_preview']
    readonly_fields = ['image_preview']
    verbose_name = "Image de la voiture"
    verbose_name_plural = "Images de la voiture"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', obj.image.url)
        return ""

    image_preview.short_description = "Aperçu de l'image"

@admin.register(Vente)
class VenteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('paid', 'user_id', 'demande_id', 'voiture_id', 'date', 'montant_total', 'montant_acompte')

@admin.register(VoitureSoumisse)
class VoitureSoumisseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('date_poste', 'user_id', 'first_name', 'last_name', 'email', 'phone', 'marque', 'modele', 'annee_fabrication', 'carburant', 'transmission', 'kilometrage', 'description', 'prix')

class MarqueResource(resources.ModelResource):
    class Meta:
        model = Marque
        fields = ('id', 'nom')
        export_order = ('id', 'nom')

class ModeleResource(resources.ModelResource):
    marque = Field(attribute='marque', column_name='marque_nom')

    class Meta:
        model = Modele
        fields = ('id', 'nom', 'marque')
        export_order = ('id', 'nom', 'marque')

    def dehydrate_marque(self, modele):
        return modele.marque.nom if modele.marque else 'No marque'

    def import_row(self, row, instance_loader, **kwargs):
        marque_nom = row.get('marque_nom')
        if marque_nom:
            marque, created = Marque.objects.get_or_create(nom=marque_nom)
            row['marque'] = marque.id
        else:
            row['marque'] = None
        return super().import_row(row, instance_loader, **kwargs)

@admin.register(Marque)
class MarqueAdmin(ImportExportModelAdmin):
    resource_class = MarqueResource
    list_display = ('id', 'nom')
    search_fields = ('nom',)

@admin.register(Modele)
class ModeleAdmin(ImportExportModelAdmin):
    resource_class = ModeleResource
    list_display = ('nom', 'marque')
    list_filter = ('marque',)
    search_fields = ('nom', 'marque__nom')


class DemandeAdmin(admin.ModelAdmin):
    list_display = ('service', 'client', 'date_desiree', 'status', 'genre')  # Champs à afficher dans la liste
    search_fields = ('member__user__first_name', 'member__user__last_name', 'first_name', 'last_name', 'email', 'service__nom')  # Champs de recherche
    list_filter = ('status', 'genre', 'service', 'date_desiree')  # Filtres
    readonly_fields = ('date',)  # Champs en lecture seule

    def client(self, obj):  # Fonction pour afficher le client (membre ou non-membre)
        if obj.member:
            return obj.member
        else:
            return f"{obj.first_name} {obj.last_name}"

    # Champs à afficher dans le formulaire d'édition
    fields = ('status', 'member', 'first_name', 'last_name', 'email', 'phone', 'service', 
              'voiture', 'date', 'date_desiree', 'details', 'genre', 'startLocation', 
              'endLocation', 'car_doc')

admin.site.register(Demande, DemandeAdmin)


class NotesAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'demande_id', 'vente_id', 'date', 'contenu')  # Fields to display in the list
    list_filter = ('user_id', 'demande_id', 'vente_id', 'date')  # Add filters for easier searching
    search_fields = ('contenu',)  # Allow searching by note content

    # You can customize further with fields like raw_id_fields for better foreign key selection

admin.site.register(Notes, NotesAdmin) 


from .models import UserWishlist

class UserWishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_voitures')  # Afficher l'utilisateur et les voitures

    def get_voitures(self, obj):
        return ", ".join([voiture.modele.nom for voiture in obj.voiture.all()])  # Afficher les noms des voitures
    get_voitures.short_description = 'Voitures'  # Nom de la colonne

admin.site.register(UserWishlist, UserWishlistAdmin)