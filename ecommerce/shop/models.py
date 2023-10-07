from django.db import models
from django.contrib.sessions.models import Session
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager




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

class BaseProduct(models.Model):
    title = models.CharField(max_length=300)
    sku = models.CharField(max_length=100, unique=True, null=False, blank=False)
    short_description = models.CharField(max_length=1000, blank=True, default="")
    price = models.FloatField(null=False, blank=False, default=0.00)
    
    class Meta:
        abstract = True
    
    
class Product(BaseProduct):
    
    # title = models.CharField(max_length=300)
    # sku = models.CharField(max_length=100, unique=True, null=False, blank=False)
    # short_description = models.CharField(max_length=1000, blank=True, default="")
    # price = models.FloatField(null=False, blank=False, default=0.00)
    online = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    
    @property
    def quantity(self):
        return self.itm_quantity.order_by('-id').first()
    
    @property
    def image(self):
        image_url = f"{settings.MEDIA_URL}/img/products/default_no_img.jpg"
        # print(f"self.images -------------------------------------- {self.images}")
        if self.images.exists():
            image_url = f"{self.images.first().image_name.url}"
        # return mark_safe(f"<img src='{image_url}' alt='product image' width='100'/>")
        return image_url
    

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
    picture = models.ImageField(upload_to=settings.CATEGORY_IMAGES_FOLDER, default="img/categories/default.png")
    online = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name}"
    
    
class ProductDescription(models.Model):
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=2500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="descriptions", null=True)
    
    def __str__(self) -> str:
        return f"{self.product.title}"    

class ProductAttributes(models.Model):
    property = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes")    
     
    def __str__(self):
        return f"{self.property} - {self.value}"

class ShoppingBasket(models.Model):
    
    product = models.OneToOneField(Product, on_delete=models.CASCADE, unique=True, null=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        
        if not extra_fields.get('is_superuser'):
            extra_fields.setdefault("is_active", False)
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    
    username = None
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

class DeliveryAddress(models.Model):
    pass

class BillingAddress(models.Model):
    pass    
    
class Order(models.Model):
    
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.DO_NOTHING)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.DO_NOTHING)
    @property
    def get_order_number(self):
        return str(self.id).zfill(10)

class OrderItems(BaseProduct):
    order = models.ForeignKey(Order, on_delete=models.PROTECT) 
    
    
    