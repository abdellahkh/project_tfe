from django.urls import path, include
from api import admin
from .views import get_voiture, add_voiture, get_voiture_status

urlpatterns = [
    path('voitures/', get_voiture),
    path('voitures/<str:status>', get_voiture_status),
    path('voitures/add/', add_voiture)
]