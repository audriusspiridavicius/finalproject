from django.contrib import admin

from .models import CustomUser, Product, ProductDescription, ProductPrices, ProductQuantity, ProductLocation
from .models import Category, ProductImages, ProductAttributes, ShoppingBasket
from .models import Order, OrderItems, DeliveryAddress


class ProductAttributesInline(admin.TabularInline):
    model = ProductAttributes
    min_num = 0
    extra = 0
    
class ProductDescriptionInline(admin.StackedInline):
    model = ProductDescription
    min_num = 1
    extra = 0
    
class ProductImagesInline(admin.StackedInline):
    model = ProductImages
    min_num = 1
    extra = 0
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductDescriptionInline,ProductImagesInline,ProductAttributesInline]
    list_display = ['title', 'sku', 'image', 'online']
    # list_display = ['title', 'sku', 'quantity', 'image', 'online']
    # list_display = ['title', 'sku', 'quantity']
    list_editable = ['online']
    
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["sku"]
        else:
            return []
        
        
    # def quantity(self,*args):
    #     return f"{Product.gquantity}"

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name','picture','online']
    list_editable = ['online']

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    exclude = ['account','unique_link_id']

class OrderLines(admin.TabularInline):
    model = OrderItems
    min_num = 1
    extra = 0
    max_num = 0
    readonly_fields = ['title', 'price', 'sku']
    can_delete = False
    

class DeliveryInline(admin.StackedInline):
    model = DeliveryAddress


class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderLines]
    
    
class ProductQuantityAdmin(admin.ModelAdmin):
    model = ProductQuantity
    list_display = ['product_title','product_sku','quantity','location']


    def product_title(self,obj):
        return obj.product.title

    def product_sku(self, obj):
        return obj.product.sku
    
    def location(self, obj):
        return obj.location.location_name

        
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductQuantity, ProductQuantityAdmin)
admin.site.register(ProductDescription)
admin.site.register(ProductPrices)
admin.site.register(ProductLocation)

admin.site.register(Category, CategoryAdmin)

admin.site.register(ShoppingBasket)
admin.site.register(CustomUser,CustomUserAdmin)


admin.site.register(Order, OrderAdmin)
