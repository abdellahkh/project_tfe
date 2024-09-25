from django.shortcuts import render, get_object_or_404
from .cart import Cart
from car_dealer.models import Voiture
from django.http import JsonResponse
from django.contrib import messages


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
        # response = JsonResponse({'Voiture ID:': voiture.id})
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