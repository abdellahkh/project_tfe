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
    path('voitures/', views.allVoitures, name='voitures'),
    path('addVoiture/', views.addVoiture, name='addVoiture'),
    path('voitures/edit/<int:voiture_id>', views.voitureEdit, name='voitureEdit'),
    path('sale_add_car/', views.saleAddCar, name='saleAddCar'),

    path('vendre/', views.vendre, name='vendre'),
    path('services/<int:service_id>', views.service, name='service_detail'),
    path('contact/<int:voiture_id>', views.contact_vehicule, name='contact_vehicule'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('demande/<int:demande_id>', views.demandeDetails, name='demande_details'),
    path('vente/<int:vente_id>', views.vente_details, name='vente_details'),
    path('vente_p/<int:vente_id>', views.vente_payer, name='vente_payer'),
    path('checkout/', views.checkout, name='checkout'),  

    path('checkout/<int:vente_id>/', views.CheckoutSessionRest.as_view(), name='checkout_session_rest'),
    path('pay_success/', views.pay_success, name='pay_success'),
    path('pay_success_accompte/', views.pay_success_accompte, name='pay_success_accompte'),
    path('vente/<int:vente_id>/ajouter_note/', views.ajouter_note, name='ajouter_note'),
    path('demande/<int:demande_id>/ajouter_note/', views.ajouter_note_demande, name='ajouter_note_demande'),
    path('vente/<int:demande_id>/ajouter_note/', views.ajouter_note_vente, name='ajouter_note_vente'),
    path('new_vente/<int:demande_id>/', views.startVente, name='start_vente'),
    path('delivery/<int:voiture_id>/<int:demande_id>/', views.car_delivery, name='car_delivery'),
    path('delivery/<int:voiture_id>/', views.car_deliveryDirect, name='car_deliveryDirect'),
    path('new_vente_service/<int:demande_id>/', views.startVenteService, name='startVenteService'),

    path('venteCancel/<int:vente_id>/', views.annuleVente, name='annuleVente'),
    path('venteCanceladmin/<int:vente_id>/', views.annuler_vente_admin, name='annuler_vente_admin'),

    path('addFavoriteCar/<int:voiture_id>/', views.toggleFavoriteCar, name='toggleFavoriteCar'),
    path('facture_pdf/<int:vente_id>/', views.vente_facture_pdf, name='facture_pdf'),
    path('recu_accomte_pdf/<int:vente_id>', views.recu_accomte_pdf, name='recu_accomte_pdf'),
    path('services/<int:service_id>/ajouter_commentaire/', views.ajouter_commentaire, name='ajouter_commentaire'),
    

]
