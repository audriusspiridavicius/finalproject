from django.urls import path, include, re_path
from .views import ProductsList, ProductListCreate, ProductUpdate, ProductBySku, ProductByOnlineStatus

urlpatterns = [
    path('api/products', ProductsList.as_view()),
    path('api/products/create', ProductListCreate.as_view()),
    path('api/<int:pk>/update', ProductUpdate.as_view()),
    re_path('^api/product/(?P<sku>.+)/$', ProductBySku.as_view()),
    re_path('^api/products/(?P<online>.+)/$', ProductByOnlineStatus.as_view()),
]