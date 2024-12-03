from django.urls import path, include
from api import admin
from .views import api_root, get_users, get_voiture, add_voiture, get_voiture_status

urlpatterns = [
    path('', api_root, name='api_root'),  
    path('voitures/', get_voiture, name='get_voiture'), 
    path('voitures/<str:status>/', get_voiture_status, name='get_voiture_status'), 
    path('voitures/add/', add_voiture, name='add_voiture'),  
    path('members/', get_users , name='get_users'),

]