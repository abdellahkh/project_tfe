from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/<username>', views.profile, name='profile'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('about/', views.about, name='about'),
    path('services/', views.allServices, name='services'),
    path('voiture/<int:pk>', views.voiture, name='voiture'),

]
