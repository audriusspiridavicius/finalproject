from typing import Any
from django.shortcuts import render
from django.views import generic
from .models import Product, Category, ProductAttributes
from django.db.models import Q
# Create your views here.


class HomepageView(generic.ListView):
    template_name = 'homepage.html'
    model = Product
    
    
class CategoriesView(generic.ListView):
    template_name = 'categories.html'
    model = Category
    context_object_name = 'categories'
    queryset = Category.objects.filter(online=True)
    
    
class ProductsView(generic.ListView):
    template_name = 'products.html'
    model = Product
    context_object_name = "products"    
    
    def get_queryset(self):
        cat_id = self.kwargs['pk']
        
        selected_attributes = self.request.GET.getlist('attr')
        
        my_filter_qs = Q()
        for attribute_value in selected_attributes:
            my_filter_qs = my_filter_qs | Q(value=attribute_value)
        products_attributes = ProductAttributes.objects.filter(my_filter_qs)
        
        
        filtered_products = Product.objects.filter(categories__in=[cat_id], online=True)
        filtered_products = filtered_products.filter(attributes__in=[id for id in products_attributes]).distinct()

        return filtered_products
    
    
    
    
class CategoryProductsView(generic.ListView):
    template_name = 'category_products.html'
    model = Product
    context_object_name = "products"
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs['pk']
        context["cat_id"] = cat_id
        selected_attributes = self.request.GET.getlist('attr')
        

        products_in_categorty = Product.objects.filter(categories__in=[cat_id], online=True)

        property_keys = ProductAttributes.objects.filter(product__in=products_in_categorty).values_list('property',flat=True).distinct()
        property_values = ProductAttributes.objects.filter(product__in=products_in_categorty).values('property','value').distinct()
        
        category_attributes = {}
        for prop in property_keys:
            category_attributes[prop] = \
            [{"value":val['value'], "selected":val['value'] in selected_attributes } for val in property_values if val['property']==prop]
        
        # print(f"custom dict {category_attributes}")
        # context["only_property"] = property_keys
        # context["only_values"] = property_values
        # context['aaaa'] = attr
        
        context['attributes'] =  category_attributes

        return context
    
    def get_queryset(self):
        return None
    
    