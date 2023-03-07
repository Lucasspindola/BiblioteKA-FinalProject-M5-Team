from rest_framework.pagination import PageNumberPagination


class CustomBookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "perPage"
    max_page_size = 20
