from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View, generic
from .models import Product, Category, ProductAttributes, ShoppingBasket, CustomUser
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.contrib.sessions.models import Session
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Count
from django.views.generic.edit import FormMixin

from django.contrib import messages
from .forms import RegistrationForm
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

class HomepageView(generic.ListView):
    template_name = 'homepage.html'
    model = Product
    
    
class CategoriesView(generic.ListView):
    template_name = 'categories.html'
    model = Category
    context_object_name = 'categories'
    queryset = Category.objects.filter(online=True)
    
    
class ProductsListView(generic.ListView):
    template_name = 'products.html'
    model = Product
    context_object_name = "products"    
    
    def get_queryset(self):
        cat_id = self.kwargs['pk']
        
        selected_attributes = self.request.GET.getlist('attr')
        
        my_filter_qs = Q()
        for attribute_value in selected_attributes:
            my_filter_qs = my_filter_qs | Q(value=attribute_value)
        products_attributes = ProductAttributes.objects.filter(my_filter_qs)
        
        
        filtered_products = Product.objects.filter(categories__in=[cat_id], online=True)
        if products_attributes:
            filtered_products = filtered_products.filter(attributes__in=[id for id in products_attributes]).distinct()

        return filtered_products
    
class CategoryProductsView(generic.ListView):
    template_name = 'category_products.html'
    model = Product
    context_object_name = "products"
    
    
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs['pk']
        context["cat_id"] = cat_id
        selected_attributes = self.request.GET.getlist('attr')
        
        products_in_categorty = Product.objects.filter(categories__in=[cat_id], online=True)

        property_keys = ProductAttributes.objects.filter(product__in=products_in_categorty).values_list('property',flat=True).distinct()
        property_values = ProductAttributes.objects.filter(product__in=products_in_categorty).values('property','value').distinct()
        
        category_attributes = {}
        for prop in property_keys:
            category_attributes[prop] = \
            [{"value":val['value'], "selected":val['value'] in selected_attributes } for val in property_values if val['property']==prop]
        

        
        context['attributes'] =  category_attributes


        return context
    
    
class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product.html'
    
    def get_queryset(self):
        
        product_id = self.kwargs['pk']
        
        product = Product.objects.filter(id=product_id, online=True)
        
        return product


class ShoppingBasketListView(generic.ListView):
    model = ShoppingBasket
    template_name = 'shoppingbasket.html'
    

class ShoppingBasketTable(generic.ListView):    
    template_name = 'shoppingcarttable.html'
    model = ShoppingBasket
    context_object_name = 'shoppingbasket'
    def get_queryset(self):

        products_in_cart = ShoppingBasket.objects.\
        filter(session=self.request.session.session_key).\
        select_related('product').all()
        
        return products_in_cart


class ShoppingBasketDeleteProduct(View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        
        product_to_delete = ShoppingBasket.objects.filter(product__id=product_id,session__session_key=self.request.session.session_key)
        
        print(f"product_to_delete = {product_to_delete}")
        print(f"product_to_delete = {product_to_delete}")
        
        product_to_delete.delete()

        return redirect('shopping_cart_table')


class CustomerRegistrationView(FormView,FormMixin):
    model = User
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('registration_successful')


    def get(self, request):
        if request.user.is_authenticated:
            return redirect('homepage')
        
        form = self.get_form()

        return render(request,'registration.html',{"form":form})
    
    def form_valid(self, form):
        
        
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        password2 = form.cleaned_data['password2']
        
        user_exist = User.objects.filter(email=email)
        
        if not user_exist:
            if password == password2:
                usr = User.objects.create_user(email=email, password=password)
                # usr.is_active = False
                usr.save()
                
            else: 
                messages.error(self.request, 'Slaptažodžiai nesutampa!')
                return redirect('registration')
        else:
            messages.error(self.request, 'Toks Vartotojas jau egzistuoja')
            return redirect('registration')
        

        return super(CustomerRegistrationView, self).form_valid(form)




def ShopingBasketUpdate(request, product_id):
    
    product = Product.objects.filter(id=product_id).first()
    
    shopping_basket = ShoppingBasket.objects.filter(product__id=product_id,session__session_key=request.session.session_key)
    
    if shopping_basket:
       print("existuoja")
    #    shopping_basket.update() 
    else:
        session = Session.objects.filter(session_key=request.session.session_key).first()
        print(f"session = {session}")
        ShoppingBasket.objects.create(product=product,session=session) 
           
    
    return redirect('mini-shopping-basket')

@require_http_methods(['GET'])
def mini_shopping_basket(request):
    
    total = {"total_sum": 0, "total_count":0}
    cart = ShoppingBasket.objects.filter(session__session_key=request.session.session_key)
    if cart:
        total = cart.all().select_related().aggregate(total_sum=Sum('product__price'),total_count=Count('product'))

    return render(request, 'mini_shopping_basket.html', total)

def confirm_registration(request, email, id):
    
    user = User.objects.filter(email=email, unique_link_id=id, is_active=False).first()
    
    if user:
        user.is_active = True
        user.unique_link_id = None
        user.save()
        return redirect('login')
        
def registration_successful(request):
    return render(request,'registration_confirm_letter_sent.html')