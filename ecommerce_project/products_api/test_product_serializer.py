from django.test import TestCase
from shop.models import Product, ProductLocation, ProductQuantity, Category
from products_api.serializers import ProductSerializer, LocationSerializer, CategorySerializer
from rest_framework.serializers import ValidationError
from django.db.models import Prefetch
class TestProductSerializer(TestCase):
    



    @classmethod
    def setUpTestData(cls) -> None:
        
        Category.objects.create(name = "test category", description = "test category test description")
        Category.objects.create(name = "test category 2 ", description = "test category 2 test description 2")
        
        
        
        cls.valid_product_data = {}

        cls.valid_product_data["sku"] = "test-product_sku_01"
        cls.valid_product_data["title"] = "Some random_product title"
        cls.valid_product_data["price"] = 19
        cls.valid_product_data["online"] = True
        cls.valid_product_data["categories"] = [1,2]
        # cls.valid_product_data["categories"] = []
        cls.valid_product_data["short_description"] = ""
        cls.valid_product_data["product_quantity"] = [
            {
                "quantity": 16,
                "location": {
                    "location_name": "test location1",
                    "address": "test location1 address!!"
                }
            }
        ]
        cls.valid_product_data["images"] = []

        cls.product_serializer = ProductSerializer(data=cls.valid_product_data)
        

        return super().setUpTestData()

    def _save_product_serializer(self):

        if self.product_serializer.is_valid():
            self.product_serializer.save()
        else:
            print(self.product_serializer.errors)

    def test_product_is_valid(self):

        self.assertEqual(True,self.product_serializer.is_valid())
    
    def test_product_sku_invalid_01(self):
        self.valid_product_data["sku"] = "test-product_sku_01"

        
       
        self.assertEquals(True,self.product_serializer.is_valid())

    def test_product_sku_invalid_02(self):
        self.valid_product_data["sku"] = "test-product__01"
        self.product_serializer = ProductSerializer(data=self.valid_product_data)
       
        self.assertEquals(False,self.product_serializer.is_valid())
             
    def test_product_sku_invalid_03(self):
        self.valid_product_data["sku"] = "test-product_sku"
        self.product_serializer = ProductSerializer(data=self.valid_product_data)

        is_valid = self.product_serializer.is_valid()

        self.assertEqual(False,is_valid)
    
    def test_product_Name_no_upper_case_leter(self):

        self.valid_product_data["title"] = "missing upper case letter text"
        self.product_serializer = ProductSerializer(data=self.valid_product_data)

        with self.assertRaises(ValidationError):
            self.product_serializer.is_valid(raise_exception=True)

    def test_product_name_min_words_count(self):

        self.valid_product_data["title"] = "Missingdsfsdf_"
        self.product_serializer = ProductSerializer(data=self.valid_product_data)

        self.assertEqual(False, self.product_serializer.is_valid())

        with self.assertRaises(ValidationError):
            self.product_serializer.is_valid(raise_exception=True)
    
    def test_product_name_contains_value_validation(self):
        self.valid_product_data["title"] = "Missin gdsfsdf"
        self.product_serializer = ProductSerializer(data=self.valid_product_data)

        self.assertFalse(self.product_serializer.is_valid())

        with self.assertRaises(ValidationError):
            self.product_serializer.is_valid(raise_exception=True)
    
    def test_product_name_empty_value(self):
        self.valid_product_data["title"] = ""
        self.product_serializer = ProductSerializer(data=self.valid_product_data)

        self.assertFalse(self.product_serializer.is_valid())

        with self.assertRaisesMessage(ValidationError, expected_message="This field may not be blank"):
            self.product_serializer.is_valid(raise_exception=True)
    
    def test_valid_number_categories_selected(self):
        self.valid_product_data["categories"] = [1,2]

        self.assertTrue(self.product_serializer.is_valid())
    
    def test_in_valid_number_categories_selected(self):
        self.valid_product_data["categories"] = [1]
        
        self.assertFalse(self.product_serializer.is_valid())

    # def test_same_category_selected_multiple_times(self):
    #     # for now it will allow add same category product. fix it later

        
    #     self.valid_product_data["categories"] = [1,1,1]
        
    #     self.assertFalse(self.product_serializer.is_valid())
    
    def test_product_created(self):

        self._save_product_serializer()
        
        product_exists = Product.objects.filter(sku=self.valid_product_data["sku"]).exists()
        
        self.assertTrue(product_exists)
    
    def test_one_product_created(self):
        
        self._save_product_serializer()
        
        products_count = Product.objects.filter(sku=self.valid_product_data["sku"]).all().count()
        
        self.assertEqual(1,products_count)    
    
    def test_new_categories_created(self):

        self._save_product_serializer()
            
        product = Product.objects.filter(sku=self.valid_product_data["sku"]).prefetch_related("categories")
        if product.exists():
            product = product.first().categories.count()
        else:
            product = None
        self.assertEqual(2,product)    

    def test_product_quantity_records_saved_database(self):
        
        self._save_product_serializer()

        products = Product.objects.filter(sku=self.valid_product_data["sku"]).prefetch_related("product_quantity")

        product_quantity_saved = products.first().product_quantity.count()

        self.assertEqual(1,product_quantity_saved)


    def test_new_location_saved_in_db(self):

        self._save_product_serializer()

        product:Product = Product.objects.filter(sku=self.valid_product_data["sku"])\
        .prefetch_related(Prefetch("product_quantity__location"))

        location_name = product[0].product_quantity.all()[0].location.location_name

        self.assertEqual("test location1", location_name)
