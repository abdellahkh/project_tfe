
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

        