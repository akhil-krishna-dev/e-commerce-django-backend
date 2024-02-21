from .serializers import WishlistSerializer
from .models import Wishlist
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from Home.models import ProductVariant


class WishlistView(ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)
    
    @api_view(['POST'])
    def in_wishlist(request):
        user = request.user
        if user.is_authenticated:
            if request.method == 'POST':
                product_variant_id = request.data['product_variant']
                product_variant = ProductVariant.objects.get(id=product_variant_id)
                if Wishlist.objects.filter(user=user,product_variant=product_variant):
                    return Response(data={"in_wishlist":True})
                else:
                    return Response(data={"in_wishlist":False})
        else:
            return Response(data={"message":"login required"})


        
class AddToWishlistView(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def create(self, validated_data):
        user = self.request.user
        product_variant = ProductVariant.objects.get(id=validated_data.data['product_variant'])
        if Wishlist.objects.filter(user=user,product_variant=product_variant):
            return Response(data={'message':'product already in wishlist'})

        wishlist = Wishlist(
            user=user,
            product_variant=product_variant
        )
        wishlist.save()
        return Response(data=validated_data.data)
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related(
            'product_variant'
        )
    

@api_view(['POST'])
def delete_wishlist(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        if request.method == 'POST':
            wishlist = Wishlist.objects.get(id=data['wishlist_id'])
            if wishlist:
                wishlist.delete()
                return Response(data={"message":"wishlist item deleted"},status=200)
