from rest_framework import viewsets
from .serializers import ProductVariantSerializer,CategorySerializer
from .models import ProductVariant,Category
from rest_framework.permissions import AllowAny
from django.db.models import Q

class ProductVariantView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ProductVariantSerializer

    def get_queryset(self):
        if self.request.query_params.get('query'):
            query = self.request.query_params.get('query')
            products = ProductVariant.objects.all().filter(
                Q(product_color_variant__product__name__icontains=query)|
                Q(product_color_variant__product__category__name__icontains=query)|
                Q(product_color_variant__product__search_keywords__icontains=query))
            return products.order_by('stock')
        
        return ProductVariant.objects.all().order_by('stock')

      
class CategoryView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('slug')