from typing import Any
from rest_framework import serializers, fields
from shop.models import Product, Category, ProductQuantity, ProductLocation, ProductImages
import random


class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImages
        fields = [ "type",'product_image']
        
        
    product_image = serializers.SerializerMethodField('get_product_image')
    def get_product_image(self, obj):
        
        print(f"testuuojam {obj.image_name}")
        print(f"testuuojam {obj}")
        print(f"testuuojam {obj}")
        return obj.image_name.url    
    

        
        
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
    
    images = ProductImageSerializer(read_only=False, many=True,allow_null=True, required=False)
    product_quantity = ProductQuantitySerializer(read_only=False, many=True)

    categories = serializers.PrimaryKeyRelatedField(many=True, queryset = Category.objects)
    anything_you_like_count = serializers.SerializerMethodField()

    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Product

        fields = ['sku','title','price','online','categories',
                  'anything_you_like_count', 'short_description', 'product_quantity', 'images']

    def get_anything_you_like_count(self, obj):
        return random.randint(0,10)
    
    # def get_product_image(self, product):
    #     return product.images.image_name.url    
    def validate_price(self, value):
        
        if value <=0:
            raise serializers.ValidationError("Price has to be larger than zero!")
        return value
    
    def create(self, validated_data):
        
        product_quantity = validated_data.pop('product_quantity')
        location_data = product_quantity.pop('location')
        categories = validated_data.pop('categories')
        
        # images = validated_data.pop('images')
        
        product = Product.objects.create(**validated_data)
        
        product.categories.set(categories)
        # location = ProductLocation.objects.create(**location_data)
        # location = ProductLocation.objects.bulk_create(location_data)
        print(type(location_data))
        print(f"location data = {location_data}")
        
        
        # for selected_location in location_data:
            # location = ProductLocation.objects.filter(id=selected_location.id)
            # location = get_object_or_404(ProductLocation, pk=selected_location.id)
        new_product_quantity = ProductQuantity.objects.create(product=product,location=location_data,**product_quantity)
        # new_product_quantity.location.set(location_data)
        
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

        
        
    
class UpdateProductDescriptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['short_description']
        

    
