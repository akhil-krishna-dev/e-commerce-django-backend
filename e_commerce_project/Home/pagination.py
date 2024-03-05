from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 50

    def paginate_queryset(self, queryset, request, view=None):

        if request.query_params.get('product_id'):
            return None
        
        if request.path == '/api/product-variants/':
            return super().paginate_queryset(queryset, request, view)

        return None