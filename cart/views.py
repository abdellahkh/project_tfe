from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .cart import Cart
from car_dealer.models import Voiture, Vente
from django.http import JsonResponse
from django.contrib import messages
import stripe 
from django.conf import settings
from django.http import JsonResponse
from django.views import View


stripe.api_key = settings.STRIPE_SECRET_KEY


def cart_summary(request):
    cart = Cart(request)
    cart_voitures = cart.get_prods
    totaltvac, total_10pourcent_tvac, sold_restant_tvac, tot_tva, tva_total_10pourcent, total_htva, tva_sold_restant, accompte_htva, sold_restant_htva  = cart.cart_total()  
    return render(request, "cart_summary.html", {"cart_voitures": cart_voitures, "totaltvac": totaltvac, "total_10pourcent_tvac": total_10pourcent_tvac, "sold_restant_tvac": sold_restant_tvac, "tot_tva": tot_tva, "tva_total_10pourcent": tva_total_10pourcent, "total_htva": total_htva, "tva_sold_restant": tva_sold_restant, "accompte_htva": accompte_htva, "sold_restant_htva": sold_restant_htva })
    
    
def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        voiture_id = int(request.POST.get('voiture_id'))
        voiture = get_object_or_404(Voiture, id=voiture_id)

        cart.add(voiture=voiture)

        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request,("Véhicule ajouté à votre sélection..."))
        return response

    

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        voiture_id = int(request.POST.get('voiture_id'))
        cart.delete(voiture=voiture_id)
        response = JsonResponse({'voiture': voiture_id})
        messages.success(request,("Véhicule retiré de votre sélection..."))
        return response



def cart_update(request):
    pass


############################### to here ############################### 

def checkout(request, voiture_id):
    return render(request, 'checkout.html', {})

class CheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        #  Calcul du montant total de l'acompte (10%) pour toutes les voitures du panier
        totaltvac, total_10pourcent_tvac, _, _, _, _, _, _, _ = cart.cart_total()  
        montant_accomte = int(float(total_10pourcent_tvac) * 100)  

        YOUR_DOMAIN = 'http://127.0.0.1:8000'

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f"Accompte de 10% pour votre sélection de véhicules", 
                        },
                        'unit_amount': montant_accomte,  
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/cart/pay_success',
            cancel_url=YOUR_DOMAIN + '/pay_cancel',
        )
        return redirect(session.url, code=303)
    
    


def pay_success(request):
    cart = Cart(request)
    messages.success(request, 'Paiement reusii')
    # Récupération des informations du panier
    voiture_ids = cart.cart.keys()
    voitures = Voiture.objects.filter(id__in=voiture_ids)
    totaltvac, total_10pourcent_tvac, _, _, _, _, _, _, _ = cart.cart_total()

    
    for voiture in voitures:
        Vente.objects.create(
            genre='Vente',
            paid='partially',  
            user_id=request.user,  
            voiture_id=voiture,
            montant_total=voiture.prix,
            montant_acompte=total_10pourcent_tvac,
        )
    for voiture in voitures:
        voiture.status = 'reservé'  
        voiture.save() 

    cart.clear()  

    return redirect(reverse('profile_view', kwargs={'username': request.user.username}))

def pay_cancel(request):
    return render(request, 'cancel.html')