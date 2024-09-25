from car_dealer.models import Voiture


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
        