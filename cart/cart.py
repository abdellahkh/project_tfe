from car_dealer.models import Voiture
from decimal import Decimal


class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        
        self.cart = cart

    def add(self, voiture):
        voiture_id = str(voiture.id)

        if voiture_id in self.cart:
            pass
        else:
            self.cart[voiture_id] = {'prix': str(voiture.prix)}

        self.session.modified = True

        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        voiture_ids = self.cart.keys()
        voitures = Voiture.objects.filter(id__in=voiture_ids)

        return voitures
    
    def delete(self, voiture):
        voiture_id = str(voiture)
        if voiture_id in self.cart:
            del self.cart[voiture_id]
        
        self.session.modified = True

    def cart_total(self):
        voiture_ids = self.cart.keys()
        voitures = Voiture.objects.filter(id__in=voiture_ids)
        quantities = self.cart
        totaltvac = 0
        total_10pourcent_tvac = 0 
        sold_restant_tvac = 0
        tot_tva = 0
        tva_total_10pourcent = 0
        total_htva = 0
        tva_sold_restant = 0
        accompte_htva = 0
        sold_restant_htva = 0
        for key, value in quantities.items():
            key= int(key)
            for voiture in voitures:
                if voiture.id == key:
                    totaltvac += voiture.prix
                    total_10pourcent_tvac += Decimal(voiture.prix) * Decimal('0.1')  # Utiliser Decimal pour les calculs décimaux
                    tot_tva += Decimal(voiture.prix) * Decimal('0.21')
        sold_restant_tvac = totaltvac - total_10pourcent_tvac
        total_10pourcent_tvac = total_10pourcent_tvac 
        total_htva = totaltvac - tot_tva
        tva_total_10pourcent = total_10pourcent_tvac * Decimal('0.21')
        tva_sold_restant = sold_restant_tvac * Decimal('0.21')
        accompte_htva = total_10pourcent_tvac - tva_total_10pourcent
        sold_restant_htva = sold_restant_tvac - tva_sold_restant
        return totaltvac, total_10pourcent_tvac, sold_restant_tvac, tot_tva, tva_total_10pourcent, total_htva, tva_sold_restant, accompte_htva, sold_restant_htva

        