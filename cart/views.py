from django.shortcuts import render, get_object_or_404
from .cart import Cart
from car_dealer.models import Voiture
from django.http import JsonResponse


def cart_summary(request):
    cart = Cart(request)
    cart_voitures = cart.get_prods
    return render(request, "cart_summary.html", {"cart_voitures": cart_voitures})
    
    
def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        voiture_id = int(request.POST.get('voiture_id'))
        voiture = get_object_or_404(Voiture, id=voiture_id)

        cart.add(voiture=voiture)

        cart_quantity = cart.__len__()
        # response = JsonResponse({'Voiture ID:': voiture.id})
        response = JsonResponse({'qty': cart_quantity})
        return response

    

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        voiture_id = int(request.POST.get('voiture_id'))
        cart.delete(voiture=voiture_id)
        response = JsonResponse({'voiture': voiture_id})
        return response



def cart_update(request):
    pass