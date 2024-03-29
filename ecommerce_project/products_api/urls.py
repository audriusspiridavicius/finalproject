from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from .views import ProductsList, ProductListCreate, ProductUpdate, ProductBySku, ProductByOnlineStatus, ProductFilterByDate
from .views import CategoriesListAdd, ProductPriceUpdate, ProductTitleUpdateView, ProductOnlineStatusUpdateView

from rest_framework.authtoken import views

from rest_framework.routers import DefaultRouter
from .views import OrderViewset, LocationViewSet



router = DefaultRouter()

router.register(r'api/orders', OrderViewset, basename='orders')
router.register(r'api/locations', LocationViewSet, basename='locations')


urlpatterns = [
    path('api/products', ProductsList.as_view()),
    path('api/products/create', ProductListCreate.as_view()),
    path('api/products/<int:pk>/update', ProductUpdate.as_view()),
    path('api/products/<int:pk>/price', ProductPriceUpdate.as_view()),
    re_path('^api/products/sku/(?P<sku>.+)/$', ProductBySku.as_view()),
    re_path('^api/products/online/(?P<online>.+)/$', ProductByOnlineStatus.as_view()),
    path('api/categories',CategoriesListAdd.as_view()),
    path('api/products/<str:sku>/title', ProductTitleUpdateView.as_view()),
    path('api/products/online/status/update/<sku>', ProductOnlineStatusUpdateView.as_view()),


    # path('api/products/<str:date_from>/<str:date_to>', ProductFilterByDate.as_view()),
    path('api/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls))

]+ \
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)