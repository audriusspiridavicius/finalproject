from typing import Any
from rest_framework import serializers, fields
<<<<<<< Updated upstream
from shop.models import Product, Category, ProductQuantity,ProductLocation
=======
from shop.models import Product, Category, ProductQuantity, ProductLocation, ProductImages, \
    Order, OrderItems
>>>>>>> Stashed changes
import random

class PositiveNumberValidator:
    def __call__(self, value):
        if value <= 0:
            message = "Price has to be larger than zero"
            raise serializers.ValidationError(message)
        
        
# class ProductFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
#     def get_queryset(self):
#         request = self.context.get('request', None)
#         queryset = super(ProductFilteredPrimaryKeyRelatedField, self).get_queryset()
#         if not request or not queryset:
#             return None
#         return queryset.filter()
class ProductQuantityLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLocation
        fields = ['location_name','address']


    
class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SlugRelatedField(slug_field='sku', many=True, queryset=Product.objects.all())
    
    
    class Meta:
        model = Category
        # exclude = ['products']
        fields = '__all__'
    
    
    def validate_name(self, value):
        validation_error_message = "Category name must be at least 5 characters"
        if len(value) < 5:
            raise serializers.ValidationError(validation_error_message)

class ProductQuantitySerializer(serializers.ModelSerializer):
    location = ProductQuantityLocationSerializer(read_only=False)
    
    class Meta:
        model = ProductQuantity
        fields = ['quantity','location']


class ProductSerializer(serializers.ModelSerializer):
    
    product_quantity = ProductQuantitySerializer(read_only=False)

    categories = serializers.PrimaryKeyRelatedField(many=True, queryset = Category.objects)
    anything_you_like_count = serializers.SerializerMethodField()
    date_created = fields.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%S'])
    # date_created1 = fields.DateTimeField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Product

        fields = ['sku','title','price','online','categories',
                  'anything_you_like_count', 'date_created', 'short_description', 'product_quantity']

    def get_anything_you_like_count(self, obj):
        return random.randint(0,10)
        
    def validate_price(self, value):
        
        if value <=0:
            raise serializers.ValidationError("Price has to be larger than zero!")
        return value
    
    def create(self, validated_data):
        
        product_quantity = validated_data.pop('product_quantity')
        location_data = product_quantity.pop('location')
        categories = validated_data.pop('categories')
        
        product = Product.objects.create(**validated_data)
        
        product.categories.set(categories)
        location = ProductLocation.objects.create(**location_data)

        ProductQuantity.objects.create(product=product,location=location,**product_quantity)
        
        return product
    
    def update(self, instance, validated_data):
        
        product_quantity = validated_data.pop('product_quantity')
        location_data = product_quantity.pop('location')
        categories = validated_data.pop('categories')
        
        prod = instance
        prod.categories.set(categories)
        
        prod.product_quantity.__dict__.update(**product_quantity)
        prod.product_quantity.save()
        
        prod.product_quantity.location.__dict__.update(**location_data)
        prod.product_quantity.location.save()

        prod.__dict__.update(validated_data)
        prod.save()
        return prod
        
        
    
<<<<<<< Updated upstream
=======
class UpdateProductDescriptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['short_description']
        

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['sku']
        
        
class OrdersSerializer(serializers.ModelSerializer):
    
    order_number = serializers.SerializerMethodField()
    order_items = OrderItemsSerializer(many=True, read_only=True)
    paid = serializers.CharField(read_only=True)
    
    class Meta:
        model = Order
        fields = ['order_number', 'paid','order_items']
    
    def get_order_number(self, order):
        return order.get_order_number
    
    
>>>>>>> Stashed changes
