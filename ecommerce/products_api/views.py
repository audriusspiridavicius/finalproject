from django.shortcuts import render
from rest_framework import generics
from shop.models import Product
from .serializers import ProductSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
class ProductBySku(generics.ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        
        sku =  self.kwargs['sku']
        
        product = Product.objects.filter(sku=sku)
        
        return product
class ProductByOnlineStatus(generics.ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        
        online =  self.kwargs['online']
        
        products = Product.objects.filter(online=online)
        
        return products
class ProductsList(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sku','online', 'title', 'categories__name']
    
    filter_backends = [filters.SearchFilter,DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title',]
    ordering = ['sku',]
    # filterset_fields = ('sku', 'online')
    # def get_queryset(self):
        
    #     queryset = Product.objects.all()
    #     filter_by_sku = self.request.query_params.get('sku', None)
    #     filter_by_online = self.request.query_params.get('online', None)
        
    #     if filter_by_sku:
    #         queryset = queryset.filter(sku=filter_by_sku)
            
    #     if filter_by_online:
    #         queryset = queryset.filter(online=filter_by_online)
    #     return queryset
    
class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
    

    
    # def perform_create(self, serializer):
    #    serializer.save(categories=[1,2])