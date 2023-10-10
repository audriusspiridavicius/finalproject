from .models import ShoppingBasket
from django.db.models import F
from django.db.models import Sum
class CartHelper():
    
    def __init__(self, session):
        self.session = session    
    
    
    @property
    def get_total_quantity(self):
        
        total_quantity = ShoppingBasket.objects \
        .filter(session__session_key=self.session.session_key) \
        .aggregate(total=Sum("quantity"))['total']
        
        return total_quantity
    
    @property
    def get_total_price(self):
        total_price = ShoppingBasket.objects \
        .filter(session__session_key=self.session.session_key) \
        .aggregate(total_price=Sum(F("quantity") * F("product__price")))['total_price']
        return total_price