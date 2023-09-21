from django.shortcuts import render
from django.views import generic
from .models import Product
# Create your views here.


class HomepageView(generic.ListView):
    template_name = 'homepage.html'
    model = Product