from rest_framework.pagination import PageNumberPagination

class SmallDataSet(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'items_per_page'
    max_page_size = 2