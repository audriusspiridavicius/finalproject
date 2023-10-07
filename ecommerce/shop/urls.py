
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.urls import include, path
from . import views
urlpatterns = [
     path('homepage/',views.HomepageView.as_view(), name='homepage'),
     path('',views.HomepageView.as_view()),
     path('kategorijos/', views.CategoriesView.as_view(), name='categories'),
     path('kategorija/<int:pk>', 
          views.CategoryProductsView.as_view(),
          name='category'),
     path('products/<int:pk>', 
          views.ProductsListView.as_view(),
          name='products'),
     path('product/<int:pk>', views.ProductDetailView.as_view(), name='product_page'),
     path('krepselis', views.ShoppingBasketListView.as_view(), name='shoppingbasket'),
     path('shoppingcart', views.ShoppingBasketTable.as_view(), name='shopping_cart_table'),
     path('cart/delete/<int:pk>',views.ShoppingBasketDeleteProduct.as_view(), name='shopping_cart_delete_item'),

     path('add-to-basket/<int:product_id>',views.ShopingBasketUpdate, name='add-to-basket'),


     path('cart/mini-shopping-basket',views.mini_shopping_basket, name='mini-shopping-basket'),

     path('registration/', views.CustomerRegistrationView.as_view(), name='registration'),
     path('registration/', views.CustomerRegistrationView.as_view(), name='account')

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

