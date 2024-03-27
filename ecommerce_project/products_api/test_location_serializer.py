from django.test import TestCase
from shop.models import ProductLocation
from annoying.functions import get_object_or_None
from products_api.serializers import ProductQuantityLocationSerializer

class TestProductLocationCreated(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.location = {
            "location_name": "warehouse",
            "address": "random street 15 45"
        }

        
        cls.location_serializer = ProductQuantityLocationSerializer(data=cls.location)

        cls.location_serializer.is_valid()
        cls.location_serializer.save()
        
        return super().setUpTestData()

    def test_product_location_serializer_valid(self):

        self.assertTrue(self.location_serializer.is_valid(), msg="location serializer should be valid, because valid location data passed")

    def test_product_location_created(self):

        created_location = ProductLocation.objects.filter(location_name=self.location["location_name"]).first()

        self.assertEqual(self.location["location_name"],created_location.location_name)
    
    def test_product_location_created_count(self):

        created_location_count = ProductLocation.objects.filter(location_name=self.location["location_name"]).count()

        self.assertEqual(1,created_location_count, msg="one location should be created in database")


