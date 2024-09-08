from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html

from .models import Marque, Modele, Voiture, ImageVoiture, Service, Review, Vente, Member, Demande, VoitureSoumisse

admin.site.register(Member)
#admin.site.register(Service)
admin.site.register(Review)
admin.site.register(Demande)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'is_available', 'prix', 'description')
    list_filter = ('is_available',)
    search_fields = ('nom',)
    readonly_fields = ('image',)

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

@admin.register(Voiture)
class VoitureAdmin(admin.ModelAdmin):
    list_display = ['marque', 'modele', 'annee_fabrication', 'carburant', 'transmission', 'kilometrage', 'prix', 'status']
    list_filter = ['marque', 'modele', 'carburant', 'transmission', 'status']
    search_fields = ['marque__name', 'modele__name', 'annee_fabrication', 'kilometrage']
    ordering = ['-date_poste']
    fieldsets = (
        (None, {
            'fields': ('status', 'marque', 'modele', 'annee_fabrication', 'carburant', 'transmission', 'kilometrage')
        }),
        ('Caractéristiques', {
            'fields': ('cruise_control', 'direction_assistee', 'audio_interface', 'airbags', 'air_conditionne', 
                       'siege_chauffant', 'alarm_system', 'parkassist', 'camera_recul', 'start_stop', 
                       'essui_auto', 'car_play')
        }),
        ('Description et Prix', {
            'fields': ('description', 'prix', 'prix_min')
        }),
    )
    inlines = [ImageVoitureInline]

admin.site.register(ImageVoiture)

@admin.register(Vente)
class VenteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('paid','user_id', 'demande_id', 'voiture_id', 'date', 'montant_total', 'montant_acompte')
    

@admin.register(VoitureSoumisse)
class VenteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('date_poste','user_id', 'first_name', 'last_name', 'email', 'phone', 'marque', 'modele', 'annee_fabrication', 'carburant', 'transmission', 'kilometrage', 'description', 'prix')




from import_export import resources
from import_export.fields import Field
from .models import Modele, Marque
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

# Define a resource for the Marque model
class MarqueResource(resources.ModelResource):
    class Meta:
        model = Marque
        fields = ('id', 'nom')  # Specify the fields you want to include in import/export
        export_order = ('id', 'nom')

class ModeleResource(resources.ModelResource):
    marque = Field(attribute='marque', column_name='marque_nom')

    class Meta:
        model = Modele
        fields = ('id', 'nom', 'marque')  # Include marque for import/export
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



# Admin configuration for the Marque model
@admin.register(Marque)
class MarqueAdmin(ImportExportModelAdmin):
    resource_class = MarqueResource
    list_display = ('id', 'nom')  # Display the name of the brand in the admin list
    search_fields = ('nom',)  # Add a search bar for the 'nom' field

# Admin configuration for the Modele model
@admin.register(Modele)
class ModeleAdmin(ImportExportModelAdmin):
    resource_class = ModeleResource
    list_display = ('nom', 'marque')  # Display the model name and the associated brand
    list_filter = ('marque',)  # Add a filter by brand
    search_fields = ('nom', 'marque__nom')  # Allow searching by model name and brand name

