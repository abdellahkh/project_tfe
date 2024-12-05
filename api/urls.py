from django.urls import path
from .views import (
    api_root, get_users, get_voiture, add_voiture, get_voiture_status,
    get_demandes, get_demandes_status, get_services, get_ventes
)

urlpatterns = [
    path('', api_root, name='api_root'),
    path('voitures/', get_voiture, name='get_voiture'),
    path('voitures/<str:status>/', get_voiture_status, name='get_voiture_status'),
    path('voitures/add/', add_voiture, name='add_voiture'),
    path('members/', get_users, name='get_users'),
    path('demandes/', get_demandes, name='get_demandes'),
    path('demandes/<str:status>/', get_demandes_status, name='get_demandes_status'),
    path('services/', get_services, name='get_services'),
    path('ventes/', get_ventes, name='get_ventes'),
]
