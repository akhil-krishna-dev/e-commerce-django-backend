from rest_framework import serializers
from .models import Cart
from Home.models import ProductVariant




class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude = ['user']
        depth = 4


class AddCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product_variant']

        
    def validate(self,data):
        product = ProductVariant.objects.get(id=data['product_variant'].id)
        if product.stock < 1:
            raise serializers.ValidationError("Item out of stock")
        return data
        
    def create(self, validated_data):

        user = self.context['request'].user
        product_variant = ProductVariant.objects.get(id=validated_data['product_variant'].id)

        cart = Cart.objects.filter(user=user,product_variant=validated_data['product_variant'])
        if cart:
            raise serializers.ValidationError("Product already in cart")

        price_while_order = product_variant.selling_price()
        offer_while_order = product_variant.offer
        quantity = 1
        
        cart.create(
            user=user,
            quantity=quantity,
            price_while_order=price_while_order,
            offer_while_order=offer_while_order,
            product_variant=validated_data['product_variant']
        )
        cart.first().save()
        
        return validated_data

