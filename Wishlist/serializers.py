from rest_framework import serializers
from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Wishlist
        fields = '__all__'
        depth = 4
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_id = instance.user.id
        data.pop('user',None)
        instance.user_id = user_id
        return data


class AddToWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('product_variant')

    

    


    
        