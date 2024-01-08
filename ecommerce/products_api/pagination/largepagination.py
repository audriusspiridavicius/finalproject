from rest_framework.pagination import PageNumberPagination

class LargeDataSet(PageNumberPagination):
    page_size_query_param = 'custom_page_parameter'
    max_page_size = 1000
    page_size = 6
    
    