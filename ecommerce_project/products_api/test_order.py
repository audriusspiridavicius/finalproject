from django.test import TestCase
from shop.models import CustomUser, Order, OrderItems
from products_api.serializers import OrdersSerializer, OrderItemsSerializer

class TestApiCreateNewOrder(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = {
            "email" : "audriusspiridavicius@gmail.com",
            "password": "12345"
        }
        
        CustomUser.objects.create(**cls.user)        
        
        cls.order = {
            "paid":False,
           
            "order_items": 
            [
                {  
                    "sku": "no_such_sku_product",
                    "title": "no_such_sku_product",
                    "quantity": 121,
                    "price": 1.11,
                    "short_description": "no_such_sku_product"
                }
            ],
            "user":1
        }
        
        cls.order_serializer = OrdersSerializer(data=cls.order)
        return super().setUpTestData() 
    
    
    def test_user_exist_on_database(self):

        user_exist = CustomUser.objects.filter(email=self.user.get("email",None)).exists()

        self.assertEqual(True, user_exist)
    
    
    def test_create_order_no_order_items_not_valid(self):
        
        order_items = self.order.pop("order_items")

        self.assertEqual(False, self.order_serializer.is_valid())
        
    def test_create_order_no_user_not_valid(self):
        
        user = self.order.pop("user")

        self.assertEqual(False, self.order_serializer.is_valid())

    def test_create_order_empty_order_items_valid_serializer(self):
        
        self.order["order_items"] = []


        self.assertEqual(True, self.order_serializer.is_valid())

    def test_create_order_empty_order_items_order_created(self):
        
        self.order["order_items"] = []

        if self.order_serializer.is_valid():
            self.order_serializer.save()
        
        order_exists = Order.objects.filter(id=1).exists()

        self.assertEqual(True, order_exists)  

    def test_create_order_items_not_created(self):
        
        ord = self.order

        ord["order_items"] = []

        self.order_serializer = OrdersSerializer(data=self.order)

        if self.order_serializer.is_valid():
            self.order_serializer.save()
        
        order_items_exists = OrderItems.objects.filter(order_id=1).exists()

        self.assertEqual(False, order_items_exists)

    def test_create_order_items_created(self):
        

        if self.order_serializer.is_valid():
            self.order_serializer.save()
        
        order_items_exists = OrderItems.objects.filter(order_id=1).exists()

        self.assertEqual(True, order_items_exists)    

    def test_create_order_items_created_sku_check(self):
        
        if self.order_serializer.is_valid():
            self.order_serializer.save()
        
        order_items_exists = OrderItems.objects.filter(order_id=1,sku=self.order["order_items"][0].get("sku",None)).exists()

        self.assertEqual(True, order_items_exists)


    def test_create_order_multiple_order_items_created(self):
        
        order = self.order

        another_order_item = {  
                    "sku": "test-sku-item-01",
                    "title": "test-sku-item-01",
                    "quantity": 1,
                    "price": 0.99,
                    "short_description": "test-sku-item-01"
                }


        order["order_items"].append(another_order_item)

        self.order_serializer = OrdersSerializer(data=order)


        if self.order_serializer.is_valid():
            self.order_serializer.save()
        
        order_item_number_1 = OrderItems.objects.filter(order_id=1,sku=self.order["order_items"][0].get("sku",None)).exists()
        order_item_number_2 = OrderItems.objects.filter(order_id=1,sku=self.order["order_items"][1].get("sku",None)).exists()

        self.assertEqual(True, (order_item_number_1 and order_item_number_2))
      