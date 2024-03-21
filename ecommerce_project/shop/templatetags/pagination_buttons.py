from django import template
from django.core.paginator import Paginator
register = template.Library()


@register.simple_tag
def pagination_buttons1(page,current_page_number, on_each_side=3, on_ends=2):
    paginator = Paginator(page.object_list, page.per_page)
    return paginator.get_elided_page_range(number=current_page_number, 
                                           on_each_side=on_each_side,
                                           on_ends=on_ends)