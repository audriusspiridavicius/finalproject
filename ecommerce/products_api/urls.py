from django.urls import path, include
from .views import ProductsList, ProductListCreate, ProductUpdate

urlpatterns = [
    path('api/products', ProductsList.as_view()),
    path('api/products/create', ProductListCreate.as_view()),
    path('api/<int:pk>/update', ProductUpdate.as_view()),
    
]