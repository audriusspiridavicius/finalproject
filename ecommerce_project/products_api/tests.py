# from django.test import TestCase
import unittest
# Create your tests here.
from random import randint

from  ecommerce.products_api.serializers import OrdersSerializer
from ecommerce.shop.models import OrderItems
# from serializers import OrdersSerializer, OrderItemsSerializer, OrderItems, Order

# from shop.models import Order, OrderItems


class TestOrderCrudOperations(unittest.TestCase):


    def setUp(self) -> None:
        
        self.random_number = randint(1,10000)
        
        self.new_order = {
            "paid":False,
            "user":2,
            "order_items": 
            [
                {  
                    "sku": f"no_such_sku_product_{self.random_number}",
                    "title": "no_such_sku_product_{self.random_number}",
                    "quantity": 121,
                    "price": 1.11,
                    "short_description": "no_such_sku_product_{self.random_number}"
                }
            ]
        }
        return super().setUp()
    
    def tearDown(self) -> None:




        return super().tearDown()
    
    
    def test_create_order(self):

        order_serializer = OrdersSerializer(data=self.new_order)
        
        if order_serializer.is_valid():

            ord = order_serializer.save()
            print(f"ord = {ord}")
            # order = Order.objects.filter(id=)

            orderlines = OrderItems.objects.filter()

        else:
            print("error error!!!!!!")    




        self.assertEqual(0,0)


if __name__ == '__main__':
    unittest.main()