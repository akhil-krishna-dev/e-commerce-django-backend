from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Orders,OrderAddress,Payment
from Cart.models import Cart
from Home.models import ProductVariant
from django.db import transaction
from rest_framework.decorators import api_view


User = get_user_model()


class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Orders
        fields = '__all__'
        depth = 4

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_id = instance.user.id
        data.pop('user',None)
        instance.user_id = user_id
        return data


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = '__all__'


class OrderConfirmSerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField()
    razorpay_payment_id = serializers.CharField()
    razorpay_signature = serializers.CharField()
    order_address_id = serializers.IntegerField()

    def save(self, cart_payment):
        payment_ids = cart_payment['payment_id']
        cart_ids = cart_payment['cart_id']

        for index in range(len(payment_ids)):
            try:
                payment = Payment.objects.get(id=payment_ids[index])
            except Exception as e:
                raise e
            payment.razorpay_order_id = self.data['razorpay_order_id']
            payment.razorpay_payment_id = self.data['razorpay_payment_id']
            payment.razorpay_payment_status = 'Paid'
            payment.paid = True
            payment.save()

            cart = Cart.objects.get(id=cart_ids[index])
            cart.delete()

        return self.data

class CashOnDeliverySerializer(serializers.Serializer):
    order_address_id = serializers.IntegerField()

    def save(self):
        user = self.context['request'].user
        order_address_id = self.data['order_address_id']
              
        cart = Cart.objects.filter(user=user)
        order_address = OrderAddress.objects.get(id=order_address_id)
        with transaction.atomic():
            for c in cart:
                payment = Payment.objects.create(
                    user = user,
                    price_paid = c.product_variant.selling_price(),
                    payment_mode = "Cash On Delivery" 
                )
                
                
                order = Orders.objects.create(
                    user=user,
                    order_address = order_address,
                    product_variant = c.product_variant,
                    price_was = c.product_variant.selling_price(),
                    quantiy_was = c.quantity,
                    payment = payment
                )
                order.order_id = "e-shop-"+ str(order.order_id)

                try:
                    product_variant = ProductVariant.objects.get(id=c.product_variant.pk)
                    product_variant.stock -= c.quantity
                    product_variant.save()
                except product_variant.DoesNotExist:
                    pass

                payment.save()
                order.save()
                c.delete()

        return self.data
    



