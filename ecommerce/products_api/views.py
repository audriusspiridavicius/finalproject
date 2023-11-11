from django.shortcuts import render
from rest_framework import generics
from shop.models import Product
from .serializers import ProductSerializer



class ProductsList(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
    

    
    # def perform_create(self, serializer):
    #    serializer.save(categories=[1,2])