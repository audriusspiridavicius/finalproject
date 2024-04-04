from django.contrib import admin


from .models import CustomUser, Product, ProductDescription, ProductPrices, ProductQuantity, ProductLocation
from .models import Category, ProductImages, ProductAttributes, ShoppingBasket
from .models import Order, OrderItems, DeliveryAddress
from django.core.paginator import Paginator
from django.utils.safestring import mark_safe
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


class ProductCategoryInline(admin.StackedInline):
    model = Category
    extra = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ProductDescriptionInline,ProductImagesInline, ProductAttributesInline]
    list_display = ['title', 'sku', 'image', 'online', 'status']
    list_editable = ['online']
    search_fields = ['sku',]
    actions = ["change_status_available","change_status_out_of_stock"] 
    autocomplete_fields = ['categories']
    list_per_page = 10
    actions_selection_counter = False
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["sku"]
        else:
            return []
        

    @admin.action(description="mark product as available")
    def change_status_available(self, request, queryset):
        queryset.update(status=Product.AVAILABLE)

    @admin.action(description="mark product as out of stock")
    def change_status_out_of_stock(self, request, queryset):
        self.actions_selection_counter = True
        queryset.update(status=Product.OUT_OF_STOCK)

    
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name','picture','online','view_category']
    list_editable = ['online']
    search_fields = ['name']
    actions = ['remove_all_products']
    autocomplete_fields = ['products','related_categories']

    def view_category(self, category):

        return mark_safe(f"<a target='_blank' href='{category.get_absolute_url()}' >View on website</a>")
    
    @admin.action(description="remove all products from category")
    def remove_all_products(self,request, queryset):
        
        for category in queryset:
            category.products.set([])


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

        

admin.site.register(ProductQuantity, ProductQuantityAdmin)
admin.site.register(ProductDescription)
# admin.site.register(ProductPrices)
admin.site.register(ProductLocation)

admin.site.register(Category, CategoryAdmin)

admin.site.register(ShoppingBasket)
admin.site.register(CustomUser,CustomUserAdmin)


admin.site.register(Order, OrderAdmin)




