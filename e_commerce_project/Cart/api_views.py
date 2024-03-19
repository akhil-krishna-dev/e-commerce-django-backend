from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cart
from Home.models import ProductVariant
from .serializers import CartSerializer,AddCartSerializer


class CartApiView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user).order_by('updated').select_related(
            'user',
            'product_variant__product_color_variant__product__category',
            'product_variant__product_color_variant__product__brand',
            'product_variant__product_color_variant__product',
            'product_variant__product_color_variant__color',
            'product_variant__product_color_variant',
            'product_variant__size',
            'product_variant'
        )

    @api_view(['POST'])
    def in_cart(request):      
        user = request.user
        if user.is_authenticated:
            if request.method == 'POST':
                product_variant_id = request.data['product_variant']
                product_variant = ProductVariant.objects.get(id=product_variant_id)
                if Cart.objects.filter(user=user,product_variant=product_variant):
                    return Response(data={"incart":True})
                else:
                    return Response(data={"incart":False})
                
    @api_view(['GET'])
    def cart_count(request):
        user = request.user
        if user.is_authenticated:
            cart = len(Cart.objects.filter(user=user))
            return Response(data=cart) 


class AddCartApiView(ModelViewSet):
    serializer_class = AddCartSerializer
    permission_classes = (IsAuthenticated,)

    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    


@api_view(['POST'])
def increament_cart(request):
    data = request.data
    product = ProductVariant.objects.get(id=data['product_variant_id'])
    cart = Cart.objects.get(id=data['cart_id'])
    if  cart.quantity < product.stock:
        if cart.quantity <10 :
            cart.quantity += 1
            cart.save()
            return Response(data={"message":"success"}, status=200)
        else:
            return Response(data={'message':"you can't select morethan 10 quantity"})
    else:
        return Response(data={'message':"sorry stock not available"})
    

@api_view(['POST'])
def decreament_cart(request):
    data = request.data
    cart = Cart.objects.get(id=data['cart_id'])
    if cart.quantity >1:
        cart.quantity -= 1
        cart.save()
        return Response(data={"message":"success"}, status=200)
    else:        
        return Response(data={'message':"quantity is zero"})

@api_view(['POST'])
def delete_cart(request):
    data = request.data
    cart = Cart.objects.get(id=data['cart_id'])
    if cart:
        cart.delete()
        return Response(data={"message":"success"}, status=200)
    else:        
        return Response(data={'message':"cart item doesn't exist"})

