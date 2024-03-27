from django.test import TestCase
from products_api.serializers import ProductQuantitySerializer
from shop.models import Category, Product, ProductQuantity, ProductLocation
from django.shortcuts import get_object_or_404
from annoying.functions import get_object_or_None
from copy import deepcopy
from rest_framework.serializers import ValidationError


class TestBaseClass:
    @classmethod
    def setUpTestData(cls) -> None:
        
        Category.objects.create(name = "test category", description = "test category test description")
        Category.objects.create(name = "test category 2", description = "test category 2 test description 2")

        cls.product = {
            "sku":"sku-001-L1",
            "title": "very good product",
            "short_description": "lorem ipsum",
            "online": False,
            "price":123,
        }
        cls.created_product = Product.objects.create(**cls.product)
        cls.created_product.categories.set([1,2])
        

        cls.product_quantity = {
            "quantity":1,
            "product":cls.created_product.id,
            "location":{
                "location_name":"location5",
                "address": "location5 address"
            }
        }

        return super().setUpTestData()
    
    
    def setUp(self) -> None:
        return super().setUp()


class TestCreateNewProductQuantity(TestBaseClass,TestCase):

    def test_product_exist(self):

        self.assertTrue(Product.objects.filter(sku=self.product["sku"]).exists())

    def test_categories_exist(self):

        self.assertTrue(Category.objects.filter(name="test category").exists())
        self.assertTrue(Category.objects.filter(name="test category 2").exists())

    def test_product_quantity_valid_serializer(self):

        product_quantity_serializer = ProductQuantitySerializer(data=self.product_quantity)
        
        if not product_quantity_serializer.is_valid():
            print(product_quantity_serializer.errors)
        
        self.assertTrue(product_quantity_serializer.is_valid())

    def test_product_quantity_created(self):

        product_quantity_serializer = ProductQuantitySerializer(data=self.product_quantity)

        valid_serializer = product_quantity_serializer.is_valid()
        
        if valid_serializer:
            product_quantity_serializer.save()

        product_quantity_db_record = get_object_or_None(Product,sku=self.product["sku"])

        self.assertTrue(product_quantity_db_record)


class TestInvalidQuantityField(TestBaseClass,TestCase):
    
    def setUp(self) -> None:
        
        self.pro_quantity = deepcopy(self.product_quantity)
        
        return super().setUp()
    
    def test_product_quantity_missing_quantity(self):

       
        self.pro_quantity.pop("quantity")

        product_quantity_serializer = ProductQuantitySerializer(data=self.pro_quantity)

        self.assertFalse(product_quantity_serializer.is_valid(), msg="serializer should be invalid because quantity field should be missing") 
    
    def test_product_quantity_missing_quantity_message(self):

        
        self.pro_quantity.pop("quantity")

        product_quantity_serializer = ProductQuantitySerializer(data=self.pro_quantity)

        with self.assertRaisesMessage(ValidationError, expected_message="This field is required"):
            product_quantity_serializer.is_valid(raise_exception=True)
            product_quantity_serializer.save()  

    def test_quantity_value_text_serializer_invalid(self):
        
        pro_quantity = deepcopy(self.pro_quantity)
        pro_quantity["quantity"] = "abc"

        product_quantity_serializer = ProductQuantitySerializer(data=pro_quantity)

        self.assertFalse(product_quantity_serializer.is_valid(), msg="quantity value is text. serializer should be invalid!")
        with self.assertRaisesMessage(ValidationError, expected_message="valid integer is required"):
            product_quantity_serializer.is_valid(raise_exception=True)
    
    def test_quantity_field_empty(self):
        
        pro_quantity = deepcopy(self.pro_quantity)
        pro_quantity["quantity"] = ""


        product_quantity_serializer = ProductQuantitySerializer(data=pro_quantity)

        self.assertFalse(product_quantity_serializer.is_valid(), msg="serializer validation should fail because quantity is set to empty string")


class TestLocationCreatedSuccessfully(TestBaseClass, TestCase):


    def test_location_created(self):


        product_quantity_serializer = ProductQuantitySerializer(data=self.product_quantity)

        self.assertTrue(product_quantity_serializer.is_valid(), msg="should be valid serializer because created with valid data")

        product_quantity_serializer.save()

        location = get_object_or_None(ProductLocation, location_name=self.product_quantity["location"]["location_name"])

        self.assertIsNotNone(location, msg="new location should be created!")

    def test_only_one_location_record_created(self):
        
        product_quantity_serializer = ProductQuantitySerializer(data=self.product_quantity)

        product_quantity_serializer.is_valid()
        product_quantity_serializer.save()

        locations_created = ProductLocation.objects.filter(location_name=self.product_quantity["location"]["location_name"]).count()

        self.assertEqual(1, locations_created, msg="only one new location dhould be created")



