from django.urls import path, include, re_path
from .views import ProductsList, ProductListCreate, ProductUpdate, ProductBySku, ProductByOnlineStatus, ProductFilterByDate
from .views import CategoriesListAdd
<<<<<<< Updated upstream
from rest_framework.authtoken import views
=======
from rest_framework.routers import DefaultRouter
from .views import OrderViewset



router = DefaultRouter()

router.register(r'orders', OrderViewset, basename='orders')

>>>>>>> Stashed changes
urlpatterns = [
    path('api/products', ProductsList.as_view()),
    path('api/products/create', ProductListCreate.as_view()),
    path('api/<int:pk>/update', ProductUpdate.as_view()),
    re_path('^api/product/(?P<sku>.+)/$', ProductBySku.as_view()),
    re_path('^api/products/online/(?P<online>.+)/$', ProductByOnlineStatus.as_view()),
    path('api/categories',CategoriesListAdd.as_view()),
<<<<<<< Updated upstream
    path('api/products/<str:date_from>/<str:date_to>', ProductFilterByDate.as_view()),
    path('api/api-token-auth/', views.obtain_auth_token)
=======
    # path('api/products/<str:date_from>/<str:date_to>', ProductFilterByDate.as_view()),
    path('api/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls))
>>>>>>> Stashed changes
]