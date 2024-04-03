from shop.models import Product, Category, ProductQuantity, ProductLocation, ProductImages, Order, OrderItems, CustomUser

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import uuid 
import random

from django.db.models import Sum, Count

from annoying.functions import get_object_or_None

from products_api.validators.product_serializer_validators import ContainsNumberValidator, ContainsValueValidator, \
PositiveNumberValidator, ProductNameHasUppercaseLetterValidator,\
ProductNameWordCountValidator, RequiredNumberOfRecordsValidator
     
        
class ProductQuantityLocationSerializer(serializers.ModelSerializer):
    
    def __init__(self, instance=None, data=..., **kwargs):
        
        if data is ...:
            data = {}
        else:
            # Ensure that the data is a dictionary
            data = dict(data)
        location_name = data.get("location_name",None)
        if location_name:
            location = ProductLocation.objects.filter(location_name=location_name).first()
            if location:
                instance = location
        
        super().__init__(instance, data, **kwargs)
    
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
        return value


class ProductImageSerializer(serializers.ModelSerializer):
    image_name =serializers.FileField()
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)
    class Meta:
        model = ProductImages
        fields = ['image_name','product']


class ProductQuantitySerializer(serializers.ModelSerializer):
    
    location = ProductQuantityLocationSerializer(read_only=False)
    id = serializers.ReadOnlyField()
    product = serializers.PrimaryKeyRelatedField(required=False, queryset=Product.objects.all())
    class Meta:
        model = ProductQuantity
        fields = ['id','quantity','location', 'product']    
    
    def create(self, validated_data):

        location = validated_data.pop("location")

        self.location = ProductQuantityLocationSerializer(data=location, many=False)

        if self.location.is_valid():
            self.location.save()
        else:
            print(f"location_serializer errors = {self.location.errors}")

        validated_data["location"] = self.location.instance
        return super().create(validated_data)


class ProductQuantityUpdateSerializer(ProductQuantitySerializer,serializers.ModelSerializer):
    id = serializers.CharField(write_only=True, validators=[])
  

class ProductSerializerBasicData(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[PositiveNumberValidator()])

    class Meta:
        model = Product
        fields = ['sku','title','price','online', 'date_created', 'short_description']


class ProductSerializer(ProductSerializerBasicData):
    
    product_quantity = ProductQuantitySerializer(read_only=False, many=True, required=True)

    categories = serializers.PrimaryKeyRelatedField(many=True, queryset = Category.objects.all())
    anything_you_like_count = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=False)
    title = serializers.CharField(
        validators=[
                    ProductNameHasUppercaseLetterValidator(),
                    ProductNameWordCountValidator(2),
                    ContainsValueValidator("_")])
    
    sku = serializers.CharField(
        validators=[ContainsValueValidator("-"),
                    ContainsValueValidator("sku"),
                    ContainsNumberValidator("sku value must have a number"), UniqueValidator(queryset=Product.objects, message="Such sku already exist. sku value must be unique")])
    
    class Meta:
        model = Product

        fields = ['sku','title','price','online','total_quantity','categories',
                  'anything_you_like_count', 'date_created', 'short_description', 'product_quantity', 'images']

    def get_anything_you_like_count(self, obj):
        return random.randint(0,10)
        
    def validate_price(self, value):
        
        if value <=0:
            raise serializers.ValidationError("Price has to be larger than zero!")
        return value
    
    def create(self, validated_data):

        images = validated_data.pop('images')
        product_quantity = validated_data.pop('product_quantity')
        categories = validated_data.pop('categories')

        product = Product.objects.create(**validated_data)
        product.categories.set(categories)

        for image in images:
            image["product"] = product.id
        product_image_serializer = ProductImageSerializer(data = images, many = True)

        if product_image_serializer.is_valid():
            product_image_serializer.save()
        else:
            print(f"invalid data errors = {product_image_serializer.errors}")
            print(f"invalid image data = {product_image_serializer.initial_data}")
            
        for prod_quantity in product_quantity:
            prod_quantity["product"] = product.id
        product_quantity_serializer = ProductQuantitySerializer(data=product_quantity, many=True)

        if product_quantity_serializer.is_valid():
            product_quantity_serializer.save()
        else:
            print(f"product_quantity_serializer error = {product_quantity_serializer.errors}")

        # for product_quantity_record in product_quantity:
            
        #     location_data = product_quantity_record.pop('location')
        #     location = get_object_or_None(ProductLocation,location_name=location_data.get("location_name"))
            
        #     if not location:
        #         location = ProductLocation.objects.create(**location_data)
        #     ProductQuantity.objects.create(product=product,location=location,**product_quantity_record)

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

    def to_internal_value(self, data):
        
        for value in data.items():
            if type(value) == str:
                value = value.strip()
        
        
        return super().to_internal_value(data)    
    
    def validate_categories(self,value):
        
        RequiredNumberOfRecordsValidator(2)(value)
        
        return value
    

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


class OrderItemListSerializer(serializers.ListSerializer):
    
    
    # instance - list of existing order item records in database
    # validated_data - list of new order item data 
    
    def update(self, instance, validated_data):
        
        update_error = []       
        for order_line_update in validated_data:

            sku = order_line_update.get("sku",None)
            order_id = order_line_update.get("order",None).id
            existing_order_line = [orderitem for orderitem in instance if orderitem.sku==sku and orderitem.order_id==order_id]

            if existing_order_line:

                existing_order_line = existing_order_line[0]

                existing_order_line.__dict__.update(order_line_update)
                existing_order_line.save()
            else:

                order_line_update["error"] = f"record was not found. sku={sku}, order id={order_id}"
                update_error.append(order_line_update)

        if update_error:
            update_error.insert(0,{"errors count":len(update_error)})
            # raise serializers.ValidationError(update_error)
        
        return instance
    

class OrderItemsSerializer(serializers.ModelSerializer):
    

    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=False)
    
    class Meta:
        model = OrderItems
        fields = ['sku', 'title', 'quantity', 'price','short_description', "order"]
        list_serializer_class = OrderItemListSerializer

    def create(self, validated_data):
        order = validated_data.get("order", None)
        order_number = 0

        if order:
            order_number = order.id
        sku = validated_data.get("sku",None)

        item_exist_for_order = OrderItems.objects.filter(sku=sku, order_id=order_number).exists() 
        if not item_exist_for_order:
            return super().create(validated_data)    
        
        
class OrdersSerializer(serializers.ModelSerializer):
    
    order_number = serializers.SerializerMethodField(read_only=True)
    order_items = OrderItemsSerializer(many=True,read_only=False)
    paid = serializers.BooleanField(default=False, required=False)
    number_of_items = serializers.SerializerMethodField(read_only=True)
    total_quantity = serializers.SerializerMethodField(read_only=True)

    user = serializers.PrimaryKeyRelatedField(required=True, queryset=CustomUser.objects.all())

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

        # need this because order equals not to id but order model object
        order_items = [dict(item, order=created_order.id) for item in order_items]

        order_lines = OrderItemsSerializer(data=order_items, many=True)
        
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

        products = Product.objects.filter(product_quantity__location=location).all()

        products_data = ProductSerializerBasicData(products, many=True, read_only=True)
        return products_data.data
