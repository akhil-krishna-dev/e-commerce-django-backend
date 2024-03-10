from rest_framework import serializers
from .models import ProductVariant,Category,ProductDiscription,ProductReviews
from Wishlist.models import Wishlist


class ProductVariantSerializer(serializers.ModelSerializer):
    in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = '__all__'
        depth = 4

    
    def get_in_wishlist(self, instance):

        user = self.context.get('request_user')
        wishlist = self.context['wishlist']

        if user and wishlist:
            for wl in wishlist:
                if instance.id == wl.product_variant.id:
                    return True
        return False



            
        

        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductDiscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscription
        fields = ('image','discription_title','description')


class ProductReviewSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = ProductReviews
        fields = ('product','review','user_info','date')


    def get_user_info(self, instance):
        first_name = instance.user.first_name
        last_name = instance.user.last_name
        user_name = f'{first_name} {last_name}'
        user_image = instance.user.profile_image.url

        return {
            'user_name':user_name,
            'user_image':user_image
        }