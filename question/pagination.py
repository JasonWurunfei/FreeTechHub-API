from rest_framework import pagination

class Pagination(pagination.PageNumberPagination):
    page_size = 3 
    page_query_param = 'page'
    page_size_query_param = 'num'