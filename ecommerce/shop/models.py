from collections.abc import Iterable
from django.db import models

from django.conf import settings
from django.utils.html import mark_safe
# Create your models here.

class ProductQuantity(models.Model):
     
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='itm_quantity')
    
    quantity = models.IntegerField()
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    location = models.ForeignKey("ProductLocation", on_delete=models.CASCADE) 

    def __str__(self) -> str:
        return f"{self.quantity}"
    
class ProductImages(models.Model):
    image_name = models.ImageField(upload_to=settings.PRODUCT_IMAGES_FOLDER)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='images')


    
    
class Product(models.Model):
    
    title = models.CharField(max_length=300)
    sku = models.CharField(max_length=100, unique=True, null=False, blank=False)
    short_description = models.CharField(max_length=1000, blank=True, default="")
    price = models.FloatField(null=False, blank=False, default=0.00)
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    
    @property
    def quantity(self):
        return self.itm_quantity.order_by('-id').first()
    
    @property
    def image(self):
        image_url = f"{settings.MEDIA_URL}/img/products/default_no_img.jpg"
        print(f"self.images -------------------------------------- {self.images}")
        if self.images.exists():
            image_url = f"{settings.MEDIA_URL}/{self.images.first().image_name}"
        return mark_safe(f"<img src='{image_url}' alt='product image' width='100'/>")
    

class ProductLocation(models.Model):
    location_name = models.CharField(max_length=250)
    address = models.CharField(max_length=500)    

    

class ProductPrices(models.Model):
    
    class PriceTypes(models.TextChoices):
        ONLINE = 'Online', 'Online'
        STORE = 'Store', 'at Store'
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_prices")
    price_type = models.CharField(max_length=10,
                                  choices=PriceTypes.choices,
                                  default=PriceTypes.ONLINE)
    price = models.DecimalField(decimal_places=2, max_digits=100, )
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.price}"
    
class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)           
    
    description = models.CharField(max_length=1000)
    
    products = models.ManyToManyField(Product, related_name="categories")
    
class ProductDescription(models.Model):
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=2500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="descriptions", null=True)
    
    def __str__(self) -> str:
        return f"{self.product.title}"    

class ProductAttributes(models.Model):
    property = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    
     