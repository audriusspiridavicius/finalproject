from django.contrib import admin

from .models import Product, ProductDescription, ProductPrices, ProductQuantity, ProductLocation
from .models import Category, ProductImages
# Register your models here.




class ProductDescriptionInline(admin.StackedInline):
    model = ProductDescription
    min_num = 1
    extra = 0
    
class ProductImagesInline(admin.StackedInline):
    model = ProductImages
    min_num = 1
    extra = 0
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductDescriptionInline,ProductImagesInline]
    list_display = ['title', 'sku', 'quantity', 'image', 'online']
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

        
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductQuantity)
admin.site.register(ProductDescription)
admin.site.register(ProductPrices)
admin.site.register(ProductLocation)

admin.site.register(Category, CategoryAdmin)
