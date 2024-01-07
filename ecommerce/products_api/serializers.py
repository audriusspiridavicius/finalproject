from typing import Any
from rest_framework import serializers, fields
from shop.models import Product, Category
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

class ProductSerializer(serializers.ModelSerializer):
    
    # quantity = serializers.ReadOnlyField(source='product.quantity')
    # categories = CategorySerializer(many=True)
    # categories = serializers.StringRelatedField(many=True)
    # categories = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset = Category.objects)
    anything_you_like_count = serializers.SerializerMethodField()
    # date_created = fields.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'])
    date_created = fields.DateTimeField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['sku','title','price','online','categories','anything_you_like_count', 'date_created']
    
    def get_anything_you_like_count(self, obj):
        return random.randint(0,10)
        
    def validate_price(self, value):
        
        if value <=0:
            raise serializers.ValidationError("Price has to be larger than zero!")
        return value


