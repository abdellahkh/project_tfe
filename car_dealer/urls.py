from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    #path('profile/<username>', views.profile, name='profile'),
    path('profile/<username>', views.profile, name='profile_view'),
    path('profile/<username>/edit', views.profileEdit, name='profile_edit'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('about/', views.about, name='about'),
    path('services/', views.allServices, name='services'),
    path('voiture/<int:pk>', views.voiture, name='voiture'),
    path('vendre/', views.vendre, name='vendre'),
    path('services/<int:service_id>', views.service, name='service_detail'),
    path('contact/<int:voiture_id>', views.contact_vehicule, name='contact_vehicule'),

    path('checkout/<int:voiture_id>', views.checkout, name='checkout'),
    path('checkout_session/<int:voiture_id>', views.checkout_session, name='checkout_session'),

    path('pay_success', views.pay_success, name='pay_success'),
    path('pay_cancel', views.pay_cancel, name='pay_cancel'),
]
