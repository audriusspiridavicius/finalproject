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
from .forms import RegistrationForm, DeliveryTypeForm, DeliveryDetailsForm, PaymnetTypeForm
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, BillingAddress, DeliveryAddress
from django.contrib.auth import logout
from django.contrib.auth import get_user_model

from .helper import CartHelper
# Create your views here.
import copy
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
        if selected_attributes:
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
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # return super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)

        context["total_sum"] = CartHelper(self.request.session).get_total_price
        return context

class ShoppingBasketDeleteProduct(View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        
        product_to_delete = ShoppingBasket.objects.filter(product__id=product_id,session__session_key=self.request.session.session_key)
        
        print(f"product_to_delete = {product_to_delete}")
        print(f"product_to_delete = {product_to_delete}")
        
        product_to_delete.delete()

        return redirect('shopping_cart_table')


class CustomerRegistrationView(FormView):
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
    request.session.save()
    product = Product.objects.filter(id=product_id).first()
    print(f"session key {request.session.session_key}")
    shopping_basket_item = ShoppingBasket.objects.filter(product__id=product_id,session__session_key=request.session.session_key).first()
    
    if shopping_basket_item:
       shopping_basket_item.quantity += 1
       shopping_basket_item.save()
    else:
        session = Session.objects.filter(session_key=request.session.session_key).first()
        print(f"session = {session}")
        ShoppingBasket.objects.create(product=product,session=session) 
           
    
    return redirect('mini-shopping-basket')

@require_http_methods(['GET'])
def mini_shopping_basket(request):
    
    total = {"total_sum": 0, "total_count":0}
    cart_helper = CartHelper(request.session)
    cart = ShoppingBasket.objects.filter(session__session_key=request.session.session_key)
    if cart:
        total = cart.all().select_related().aggregate(total_sum=Sum('product__price'),total_count=Count('product'))
        print(f" get_total_quantity = {cart_helper.get_total_quantity}")
        total['total_count'] = cart_helper.get_total_quantity
        total['total_sum'] = cart_helper.get_total_price
        

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


class OrderView(FormView):
    
    success_url = '/homepage'
    
    def post(self, request) :
        
        
        # these not used yet
        # delivery_type_form = DeliveryTypeForm(request.POST)
        # payment_type_form = PaymnetTypeForm(request.POST)
       
        delivery_information_form = DeliveryDetailsForm(request.POST)
        if delivery_information_form.is_valid():
        
            return self.form_valid(request.POST)
    
    def form_valid(self, form):

        # payment_type_form = PaymnetTypeForm(self.request.POST)    
        # delivery_type_form = DeliveryTypeForm(self.request.POST)
        delivery_information_form = DeliveryDetailsForm(self.request.POST)
        
        
        
        delivery_info = delivery_information_form.save()

        d=copy.deepcopy(delivery_info.__dict__)

        # need to remove _state ???
        d.pop("_state")

        billing = BillingAddress.objects.create(**d)
        user = self.request.user
        if not self.request.user.is_authenticated:
            user = User.objects.create(email='gdfdfgdfsg@gmail.com')
            user.is_active = False
            user.save()
        order = Order.objects.create(delivery=delivery_info,billing=billing, user=user )
        
        # ShoppingBasket.objects.filter(session=self.request.session.session_key).delete()
        
        
        logout(self.request)

        
        
        return super().form_valid(form)
    

    
    def get(self, request):
        
        cart = ShoppingBasket.objects.filter(session__session_key=self.request.session.session_key).all()
        
        if not cart:
            return redirect('homepage')
        if cart:
            delivery_type_form = DeliveryTypeForm()
            delivery_information_form = DeliveryDetailsForm()
            payment_type_form = PaymnetTypeForm()
            context = {
                'delivery_type_form':delivery_type_form,
                'delivery_information_form':delivery_information_form,
                'payment_form':payment_type_form
                }
            return render(request,'order/order.html', context=context)

