from rest_framework import serializers
from .models import ProductVariant,Category,ProductDiscription,ProductReviews,RecentViewedProducts


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
        fields = ('id','image','discription_title','description')


class ProductReviewSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = ProductReviews
        fields = ('id','product','review','user_info','date')


    def get_user_info(self, instance):
        first_name = instance.user.first_name
        last_name = instance.user.last_name
        user_name = f'{first_name} {last_name}'
        user_image = instance.user.profile_image.url

        return {
            'user_name':user_name,
            'user_image':user_image
        }
    


class RencentViewedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentViewedProducts
        fields = ['product']
        depth = 4

    def create(self,validated_data):
        user = self.context['request'].user
        data = self.context['request'].data

        product = data['product']

        recent_products = RecentViewedProducts.objects.filter(user=user)
        if recent_products.filter(product__id=product):
            raise serializers.ValidationError('product already in recent model')
        
        if len(recent_products) > 20:
            recent_products[0].delete()

        product_variant = ProductVariant.objects.get(id=product)
        data['product'] = product_variant
        data['user'] = user
        return super().create(data)