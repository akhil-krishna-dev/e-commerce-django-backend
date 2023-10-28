from rest_framework import viewsets
from .serializers import ProductVariantSerializer,CategorySerializer
from .models import ProductVariant,Category
from rest_framework.permissions import AllowAny


class ProductVariantView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ProductVariantSerializer
    queryset = ProductVariant.objects.all().order_by('stock')

      
class CategoryView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('slug')