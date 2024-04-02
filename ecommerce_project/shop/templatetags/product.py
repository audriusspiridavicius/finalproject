from shop.models import Product, ProductAttributes
from django import template
from django.core.paginator import Paginator
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
register = template.Library()




@register.inclusion_tag("product/product_main_info.html")
def product_main_info(product:Product):

    return {"sku":product.sku, "title":product.title, "price": product.price, "short_description": product.short_description}


@register.filter(name="price")
@stringfilter
def format_price(price):
    return mark_safe(f"{price}&euro;")



@register.simple_tag()
def display_attributes(attributes):
    result=""
    for attribute in attributes:
            result = result + f"<div>{attribute.property}:{attribute.value}</div>"

    return mark_safe(result)

@register.inclusion_tag("product/add_to_basket_button.html")
def add_to_basket_button(product_id):
     
     return {"product_id": product_id}

@register.inclusion_tag("product/attributes.html")
def product_attributes(sku):
     
    result_list = []
    attribute_names = ProductAttributes.objects.filter(product__sku=sku).values("property").distinct().all()
    attribute_values = ProductAttributes.objects.filter(product__sku=sku).values("property","value").distinct().all()
 
    print(f"attribute_names {attribute_names}")
    print(f"attribute_values {attribute_values}")


    for attribute_name in attribute_names:
        print(attribute_name)
        result_list.append({"name":attribute_name["property"],"values":[value["value"] for value in attribute_values if value["property"]==attribute_name["property"]]})
         
    print(f"result_list = {result_list}")
    return {"attribute_list": result_list}