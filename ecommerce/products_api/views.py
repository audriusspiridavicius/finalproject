from django.shortcuts import render
from rest_framework import generics

from rest_framework import generics, parsers
from shop.models import Product, Category, Order
from .serializers import ProductOnlineStatusSerializer, ProductSerializer, CategorySerializer, UpdateProductDescriptionSerializer, ProductUpdateSerializer
from .serializers import OrdersSerializer, UpdateProductPriceSerializer

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .pagination.largepagination import LargeDataSet
from .pagination.smallpagination import SmallDataSet
from rest_framework import viewsets
from .serializers import ProductTitleSerializer

from rest_framework.permissions import IsAuthenticated

import datetime

from django.shortcuts import get_object_or_404, get_list_or_404


class ProductFilterByDate(generics.ListAPIView):
    serializer_class = ProductSerializer
    
    
    def get_queryset(self):
        
        date_from = self.kwargs['date_from']
        date_to = self.kwargs['date_to']
        
        date_to = datetime.datetime.strptime(date_to,'%Y-%m-%d') + datetime.timedelta(days=1)
        
        products = Product.objects.filter(date_created__range=[date_from,date_to])
        
        
        return products
    
class ProductBySku(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = None
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
    filterset_fields = ['sku','online', 'title', 'categories__name']
    pagination_class = LargeDataSet
    filter_backends = [filters.SearchFilter,DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title','sku',]
    ordering = ['sku',]
    permission_classes = [IsAuthenticated]
    
    
class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = None
    queryset = Product.objects.all()
    # Details and limitations
    # Proper use of cursor based pagination requires a little attention to detail. You'll need to think about what ordering you want the scheme to be applied against. The default is to order by "-created". This assumes that there must be a 'created' timestamp field on the model instances, and will present a "timeline" style paginated view, with the most recently added items first.

    # In other words, you can't have all three of these conditions:

    # Using cursor pagination
    # ...without specifying an ordering
    # ...on a model without a created field

class ProductUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = ProductUpdateSerializer
    queryset = Product.objects.all()
    pagination_class = None


        
class CategoriesListAdd(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = SmallDataSet      
    permission_classes = [IsAuthenticated]
    

class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer
    pagination_class = None

class ProductPriceUpdate(generics.UpdateAPIView):
    serializer_class = UpdateProductPriceSerializer
    queryset = Product.objects.all()
    pagination_class = None    

class ProductTitleUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProductTitleSerializer
    pagination_class = SmallDataSet
    lookup_field = 'sku'

    def get_queryset(self):
        
        sku = self.kwargs['sku']
        print(f" sku value = {sku}")
        product = Product.objects.filter(sku=sku)

        # line below is wrong in this case
        # product = get_object_or_404(Product, sku=sku)
        # because get_queryset should return queryset and not model type

        return product
    
class ProductOnlineStatusUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProductOnlineStatusSerializer
    lookup_field = 'sku'
    pagination_class = None

    def get_queryset(self):
        
        sku = self.kwargs['sku']

        product = Product.objects.filter(sku=sku)

        return product

