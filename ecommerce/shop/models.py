from django.db import models
from django.contrib.sessions.models import Session
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
from django.core.mail import send_mail
import uuid
from django.template.loader import render_to_string
from django.conf import settings

from django.utils.html import strip_tags

from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User

from .manager import OrderManager


# user = get_user_model()


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
    
    product = models.OneToOneField(Product, on_delete=models.CASCADE, 
                                   unique=True, null=False, related_name='shopping_basket')
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password = None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        unique_link_id = None
        content = {}
        if not extra_fields.get('is_superuser'):
            extra_fields.setdefault("is_active", False)
            unique_link_id = str(uuid.uuid4())
            
            context = {
                'email': email,
                "unique_id": unique_link_id
            }
            
            
            content = render_to_string('confirm_registration.html', context=context)
            # content = strip_tags(content)
            # eml = EmailMessage(
            #     subject="confirm registration",
            #     message=content,
            #     from_email=settings.EMAIL_HOST_USER,
            #     recipient_list=[email],
    
            # )
            eml = EmailMessage(
                "confirm registration",
                content,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )
            eml.content_subtype = "html"
            eml.send()
        email = self.normalize_email(email)
        user = self.model(email=email,unique_link_id=unique_link_id, **extra_fields)
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
    unique_link_id = models.UUIDField(default=None, null=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

class BaseAddress(models.Model):
    
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=200)
    house_number = models.CharField(max_length=10)
    post_code = models.CharField(max_length=10)
    other_info = models.CharField(max_length=1000)
    class Meta:
        abstract = True

class DeliveryAddress(BaseAddress):
   
   pass 

class BillingAddress(BaseAddress):
   pass 


    
class Account(models.Model):
    
    delivery = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True)
    billing = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, null=True)
    
    
class ModelDate(models.Model):
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)    
    
    class Meta:
        abstract = True
    
class Order(ModelDate):
    objects = OrderManager()
    
    paid_at_Date = models.DateField(null=True)
    paid = models.BooleanField(default=False)
    
    delivery = models.ForeignKey(DeliveryAddress, on_delete=models.PROTECT, null=True)
    billing = models.ForeignKey(BillingAddress, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    

    @property
    def get_order_number(self):
        return f"ord-{str(self.id).zfill(10)}"
     
    
class OrderItems(BaseProduct, ModelDate):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sku = models.CharField(max_length=100, unique=False, null=False, blank=False)