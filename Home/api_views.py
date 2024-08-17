from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import *
from .models import ProductVariant,Category,ProductDiscription,Product,ProductReviews,RecentViewedProducts
from rest_framework.permissions import AllowAny,IsAuthenticated
from Wishlist.models import Wishlist
from django.db.models import Q
from .pagination import CustomPagination





class ProductVariantView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ProductVariantSerializer
    pagination_class = CustomPagination

    def get_serializer_context(self):
        user = self.request.user
        wishlist = None
        if user.is_authenticated:
            wishlist = Wishlist.objects.filter(user=user).select_related(
                'user',
                'product_variant'
            )
        context = super().get_serializer_context()
        context['request_user'] = user
        context['wishlist'] = wishlist
        return context


    def get_queryset(self):
        product_variants = ProductVariant.objects.all().order_by('stock').select_related(
            'product_color_variant__product__category',
            'product_color_variant__product__brand',
            'product_color_variant__product',
            'product_color_variant__color',
            'product_color_variant',
            'size'
        )


        query = self.request.query_params.get('query')
        if query:
            products = product_variants.filter(
                Q(product_color_variant__product__name__icontains=query)|
                Q(product_color_variant__product__category__name__icontains=query)|
                Q(product_color_variant__product__search_keywords__icontains=query)).select_related(
                    'product_color_variant__product__category',
                    'product_color_variant__product__brand',
                    'product_color_variant__product',
                    'product_color_variant__color',
                    'product_color_variant',
                    'size'
                )
            return products
        

        category = self.request.query_params.get('category')
        price_filter = self.request.query_params.get('price')



        if category:           
            products = product_variants.filter(
                product_color_variant__product__category__slug=category
            ).select_related(
                'product_color_variant__product__category',
                'product_color_variant__product__brand',
                'product_color_variant__product',
                'product_color_variant__color',
                'product_color_variant',
                'size'
            )
            if price_filter == 'low':
                return products.order_by('price')
            if price_filter == 'high':
                return products.order_by('-price')
            return products
        
        product_id = self.request.query_params.get('product_id')
        if product_id:         
            products = product_variants.filter(
                product_color_variant__product__id=product_id
            ).select_related(
                'product_color_variant__product__category',
                'product_color_variant__product__brand',
                'product_color_variant__product',
                'product_color_variant__color',
                'product_color_variant',
                'size'
            )
            return products

        best_deal = self.request.query_params.get('best_deal')
        if best_deal: 
            filtered_products = list(filter(lambda product: product.stock > 0 and product.offer>int(best_deal) , product_variants))
            return filtered_products       

        filtered_products = list(filter(lambda product: product.stock > 0, product_variants))       
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
        queryset = ProductDiscription.objects.filter(product__id = product_id).select_related(
            'product'
        )
        return queryset
    

class ProductReviewView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ProductReviewSerializer
    
    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')

        if product_id:
            product_reveiws = ProductReviews.objects.filter(product__id=product_id).select_related(
                'user',
                'product'
            )
            return product_reveiws



@api_view(['POST'])
def product_review_save(request):
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



class RecentViewedProductsView(viewsets.ModelViewSet):
    serializer_class = RencentViewedProductSerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        return RecentViewedProducts.objects.filter(user=self.request.user)
