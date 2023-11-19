from django.shortcuts import render, get_object_or_404
from .cart import Cart
from car_dealer.models import Voiture
from django.http import JsonResponse


def cart_summary(request):
    return render(request, "cart_summary.html", {})
    
    
def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        voiture_id = int(request.POST.get('voiture_id'))
        voiture = get_object_or_404(Voiture, id=voiture_id)

        cart.add(voiture=voiture)
        response = JsonResponse({'Voiture:':voiture.id})
        return response

    

def cart_delete(request):
    pass

def cart_update(request):
    pass