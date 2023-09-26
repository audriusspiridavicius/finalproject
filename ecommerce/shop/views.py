from django.shortcuts import render
from django.views import generic
from .models import Product, Category
# Create your views here.


class HomepageView(generic.ListView):
    template_name = 'homepage.html'
    model = Product
    
    
class CategoriesView(generic.ListView):
    template_name = 'categories.html'
    model = Category
    context_object_name = 'categories'
    queryset = Category.objects.filter(online=True)