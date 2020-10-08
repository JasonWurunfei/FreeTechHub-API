from rest_framework import pagination
from django.conf import settings

class Pagination(pagination.PageNumberPagination):
<<<<<<< Updated upstream
    page_size = 5
=======
    page_size = settings.PAGE_SIZE
>>>>>>> Stashed changes
    page_query_param = 'page'
    page_size_query_param = 'num'