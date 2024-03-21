from typing import Any
from rest_framework import serializers
from shop.models import Product, Category, ProductQuantity, ProductLocation, ProductImages, \
    Order, OrderItems, CustomUser

import random

from django.db.models import Sum, Count

from annoying.functions import get_object_or_None


class PositiveNumberValidator:
    def __call__(self, value):
        if value <= 0:
            message = "Price has to be larger than zero"
            raise serializers.ValidationError(message)
        
        
class ProductQuantityLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLocation
        fields = ['location_name','address']


    
class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SlugRelatedField(slug_field='sku', many=True, queryset=Product.objects.all())
    
    
    class Meta:
        model = Category
        fields = '__all__'
    
    
    def validate_name(self, value):
        validation_error_message = "Category name must be at least 5 characters"
        if len(value) < 5:
            raise serializers.ValidationError(validation_error_message)


class ProductQuantitySerializer(serializers.ModelSerializer):
    
    location = ProductQuantityLocationSerializer(read_only=False)
    id = serializers.ReadOnlyField()

    class Meta:
        model = ProductQuantity
        fields = ['id','quantity','location']    
    
class ProductQuantityUpdateSerializer(ProductQuantitySerializer,serializers.ModelSerializer):
    id = serializers.CharField(write_only=True, validators=[])
  
class ProductSerializerBasicData(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = ['sku','title','price','online', 'date_created', 'short_description']



class ProductSerializer(ProductSerializerBasicData):
    
    product_quantity = ProductQuantitySerializer(read_only=False, many=True)

    categories = serializers.PrimaryKeyRelatedField(many=True, queryset = Category.objects)
    anything_you_like_count = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Product

        fields = ['sku','title','price','online','total_quantity','categories',
                  'anything_you_like_count', 'date_created', 'short_description', 'product_quantity']

    def get_anything_you_like_count(self, obj):
        return random.randint(0,10)
        
    def validate_price(self, value):
        
        if value <=0:
            raise serializers.ValidationError("Price has to be larger than zero!")
        return value
    
    def create(self, validated_data):
        
        product_quantity = validated_data.pop('product_quantity')
        
        categories = validated_data.pop('categories')
        product = Product.objects.create(**validated_data)
        product.categories.set(categories)
        
        for product_quantity_record in product_quantity:
            
            location_data = product_quantity_record.pop('location')
            location = get_object_or_None(ProductLocation,location_name=location_data.get("location_name"))
            
            if not location:
                location = ProductLocation.objects.create(**location_data)
            ProductQuantity.objects.create(product=product,location=location,**product_quantity_record)

        return product
    
    def update(self, instance, validated_data):
        product_quantity = validated_data.get('product_quantity')
        prod = instance  
        for quantity_data in product_quantity:   
            
            quantity_record = get_object_or_None(ProductQuantity,id=quantity_data.get("id"))
            if quantity_record:
                location_info = quantity_data.get('location') # None if not found
                location = get_object_or_None(ProductLocation,location_name=location_info['location_name'])

                if location:
                    location_info.pop('location_name')
                    location.__dict__.update(**location_info)
                else:
                    location = ProductLocation.objects.create(**location_info)
                    quantity_record.quantity = quantity_data["quantity"]
                    quantity_record.location = location
                    quantity_record.save()

        categories = validated_data.pop('categories')
        prod.categories.set(categories)
        
        prod.__dict__.update(validated_data)
        prod.save()
        return prod
    
    def get_total_quantity(self, product):
        total_quantity_sum = product.product_quantity.all().aggregate(Sum("quantity"))["quantity__sum"] or 0
        return total_quantity_sum
        
class ProductUpdateSerializer(ProductSerializer):
    product_quantity = ProductQuantityUpdateSerializer(many=True)
    

class UpdateProductDescriptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['short_description']

class UpdateProductPriceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['price']


        
class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = CustomUser
        fields = ["email","id"]


class OrderItemsSerializer(serializers.ModelSerializer):
    

    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=False)
    # order = serializers.SlugRelatedField(many=False, queryset=Order.objects.all(), slug_field="id")
    # order_id = serializers.SlugRelatedField(many=False, queryset=Order.objects.all(), slug_field="id")
    # required=False
    
    class Meta:
        model = OrderItems
        fields = ['sku', 'title', 'quantity', 'price','short_description', "order"]
        list_serializer_class = "OrderItemListSerializer"

    def create(self, validated_data):
        print(f"OrderItemsSerializer create validated_data = {validated_data}")
        order = validated_data.get("order", None)
        order_number = 0
        if order:
            order_number = order.id
        sku = validated_data.get("sku",None)

        item_exist_for_order = OrderItems.objects.filter(sku=sku, order_id=order_number).exists() 
        if not item_exist_for_order:
            # self.errors["dsfsdafdsaf"] = {"fdadsfdsaf":"dfdsfdsafdsafadsf"}
            # validated_data["error"] = {"message": f"Such product (sku={sku}) already exists on order {order_number}"}
            # return {"message": f"Such product (sku={sku}) already exists on order {order_number}"}
            # raise serializers.ValidationError()
            # return {"message": f"Such product ({sku}) already exists on order {order_number}"}
            return super().create(validated_data)    
        
        
class OrdersSerializer(serializers.ModelSerializer):
    
    order_number = serializers.SerializerMethodField(read_only=True)
    order_items = OrderItemsSerializer(many=True,read_only=False)
    paid = serializers.BooleanField(default=False)
    number_of_items = serializers.SerializerMethodField(read_only=True)
    total_quantity = serializers.SerializerMethodField(read_only=True)
    # user = UserSerializer(read_only=True)


    class Meta:
        model = Order
        fields = ['order_number', 'paid', 'number_of_items','order_items','total_quantity', "user"]
    
    def get_order_number(self, order):
        return order.get_order_number
    
    def get_number_of_items(self, order):
        return order.order_items.count()

    def get_total_quantity(self, order):
        return OrderItems.objects.filter(order_id=order.id).aggregate(Sum('quantity'))["quantity__sum"]
    
    def __remove_related_data(self,validated_data, related_field):

        return validated_data.pop(related_field)


    def update(self, instance, validated_data):
        
        order_items = self.__remove_related_data(validated_data,"order_items")

        # need this because order equals not to id but order model object
        order_items = [dict(item, order=instance.id) for item in order_items]

        

        existing_order_lines = OrderItems.objects.filter(order_id=instance.id).all()

        orderlines = OrderItemsSerializer(instance=existing_order_lines,many=True, data=order_items)
        
        if orderlines.is_valid():
            orderlines.save()
        else:
            raise serializers.ValidationError({'message': orderlines.errors})
        
        return super().update(instance, validated_data)

    def create(self, validated_data):
        order_items = self.__remove_related_data(validated_data,"order_items")
        created_order = super().create(validated_data)
        print(f"created_order = {created_order}")
        


        # need this because order equals not to id but order model object
        order_items = [dict(item, order=created_order.id) for item in order_items]

        order_lines = OrderItemsSerializer(data=order_items, many=True)
        
        print(f"Order create validated_data = {validated_data}")
        
        # OrderItemsSerializer.create(order_lines,order_items)
        if order_lines.is_valid():
            order_lines.save()
        else:
            raise serializers.ValidationError({'message': order_lines.errors})
        
        
        return created_order
    




class OrderSerializer2(OrdersSerializer):

    class Meta:
        model = Order
        fields = ['id','user','order_items']

class ProductTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["title"]


class ProductOnlineStatusSerializer(serializers.ModelSerializer):

    sku = serializers.StringRelatedField(read_only=True)
    title = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ["online","sku", "title"]


class LocationSerializer(serializers.ModelSerializer):

    products_count = serializers.SerializerMethodField("get_location_products_count")
    products = serializers.SerializerMethodField("get_location_products")


    class Meta:
        model = ProductLocation
        fields = ["id", "location_name", "address", "products_count", "products"]


    def get_location_products_count(self, location):

        products_count = location.productquantity.all().aggregate(count=Count("product_id")).get('count')
        return products_count

    def get_location_products(self, location):

        
        # productquantities = location.productquantity.all().select_related("product")
        # products = [quantity.product for quantity in productquantities]
        # products = Product.objects.prefetch_related("product_quantity")
        # products = products.filter(product_quantity__location=location).all()
        products = Product.objects.filter(product_quantity__location=location).all()

        products_data = ProductSerializerBasicData(products, many=True, read_only=True)
        return products_data.data


class OrderItemListSerializer(serializers.ListSerializer):
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)