from rest_framework import serializers
from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'
        depth = 4
    


class AddToWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('product_variant')

    

    


    
        