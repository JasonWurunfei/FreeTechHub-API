from rest_framework import pagination
from django.conf import settings

class Pagination(pagination.PageNumberPagination):
    page_size = settings.PAGE_SIZE
    page_query_param = 'page'
    page_size_query_param = 'num'