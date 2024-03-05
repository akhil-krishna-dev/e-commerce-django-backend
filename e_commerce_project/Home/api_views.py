from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import *
from .models import ProductVariant,Category,ProductDiscription,Product,ProductReviews
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.db.models import Q
from .pagination import CustomPagination





class ProductVariantView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ProductVariantSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        product_variants = ProductVariant.objects.all().order_by('stock')
        filtered_products = list(filter(lambda product: product.stock > 0, product_variants))
        if self.request.query_params.get('query'):
            query = self.request.query_params.get('query')
            products = product_variants.filter(
                Q(product_color_variant__product__name__icontains=query)|
                Q(product_color_variant__product__category__name__icontains=query)|
                Q(product_color_variant__product__search_keywords__icontains=query))
            return products
        
        if self.request.query_params.get('category'):
            category = self.request.query_params.get('category')
            products = product_variants.filter(
                product_color_variant__product__category__slug=category
            )
            return products
        
        if self.request.query_params.get('product_id'):
            product_id = self.request.query_params.get('product_id')
            products = product_variants.filter(
                product_color_variant__product__id=product_id
            )
            return products
        
        return filtered_products

      
class CategoryView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('slug')



class ProductDescriptionView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductDiscriptionSerializer

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        queryset = ProductDiscription.objects.filter(product__id = product_id)
        return queryset
    

class ProductReviewView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductReviewSerializer
    queryset = ProductReviews.objects.all()
    
    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')

        if product_id:
            product_reveiws = ProductReviews.objects.filter(product__id=product_id)
            return product_reveiws



@api_view(['POST'])
def product_review_save(request):
    print('data ', request.data)
    product_id = request.data['product_id']
    review = request.data['reveiw']

    product = get_object_or_404(Product, id=product_id)
    review = ProductReviews.objects.create(
        user = request.user,
        product = product,
        review = review
    )
    product.save()
    return Response({'message':'review saved'})
