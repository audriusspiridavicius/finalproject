from shop.models import Order, OrderItems, CustomUser
from products_api.serializers import OrdersSerializer

from django.test import TestCase



class TestOrderCrudOperations(TestCase):


    def setUp(self) -> None:
        
        user = {
            "email": "audriusspiridavicius@gmail.com",
            "password": "1111"
        }

        self.user = user
        
        self.new_order = {
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


        CustomUser.objects.create(**self.user)

        return super().setUp()
    
    def tearDown(self) -> None:

        return super().tearDown()
    

    def test_create_new_user(self):
          
        new_user_created = CustomUser.objects.filter(email=self.user["email"]).exists()
        
        self.assertEqual(True,new_user_created)

    def test_create_new_user_not_superuser(self):
          
        new_user = CustomUser.objects.filter(email=self.user["email"]).first()
        
        self.assertEqual(False,new_user.is_superuser)

    def test_create_new_user_check_primary_key_value(self):
          
        new_user = CustomUser.objects.filter(email=self.user["email"]).first()
        
        self.assertEqual(1,new_user.id)

    def test_create_order(self):

        new_order_exist = None
        order_serializer = OrdersSerializer(data=self.new_order)
        
        if order_serializer.is_valid():  
            
            ord = order_serializer.save()
            new_order_exist = Order.objects.filter(id=ord.id).exists()

        self.assertEqual(True,new_order_exist)

    def test_create_order_order_items_created(self):

        new_order_items_exist = None
        order_serializer = OrdersSerializer(data=self.new_order)
        
        if order_serializer.is_valid():  
            
            ord = order_serializer.save()
            new_order_items_exist = OrderItems.objects.filter(order_id=ord.id).exists()

        self.assertEqual(True,new_order_items_exist)

    # def test_model_properties(self):
    #     properties = OrderItems._meta.fields
        
    #     properties = [property.name for property in properties]

        
    #     print(f"OrderItems keys = {properties}")






        # current_data_keys = [orderitem. for orderitem in instance]
        
        


        self.assertEqual(0,0)



