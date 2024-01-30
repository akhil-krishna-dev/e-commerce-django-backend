from rest_framework import serializers
from .models import Orders,OrderAddress,Payment
from Cart.models import Cart
from Home.models import ProductVariant
from rest_framework.response import Response
from django.db import transaction

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
        depth = 4


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = '__all__'


class OrderConfirmSerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField()
    razorpay_payment_id = serializers.CharField()
    razorpay_signature = serializers.CharField()
    order_address_id = serializers.IntegerField()
    # class Meta:
    #     model = Orders
    #     fields = ['order_address','razorpay_order_id','razorpay_payment_id','razorpay_signature']

    def save(self):
        total_amount = 0
        print('self area',self.data)
        user = self.context['request'].user
        order_address_id = self.data['order_address_id']
        razorpay_order_id = self.data['razorpay_order_id']
        razorpay_payment_id = self.data['razorpay_payment_id']
        razorpay_signature = self.data['razorpay_signature']
        order_address = OrderAddress.objects.get(id=order_address_id)
        with transaction.atomic():
            cart = Cart.objects.filter(user=user)
            for c in cart:
                payment = Payment.objects.create(
                    user=user,
                    price_paid = c.product_variant.orginal_price(),
                    payment_mode = "RazorPay",
                    razorpay_order_id = razorpay_order_id,
                    razorpay_payment_status = "Paid",
                    razorpay_payment_id = razorpay_payment_id,
                    paid = True,
                )

                order = Orders.objects.create(
                    user = user,
                    order_address = order_address,
                    product_variant = c.product_variant,
                    price_was = c.product_variant.orginal_price(),
                    quantiy_was = c.quantity,
                    payment = payment
                )
                order.order_id = "akhil "+ str(order.order_id)
                try:
                    product_variant = ProductVariant.objects.get(id=c.product_variant.pk)
                    product_variant.stock = (product_variant.stock - c.quantity)
                    product_variant.save()
                except product_variant.DoesNotExist:
                    pass
                payment.save()
                order.save()
                c.delete()
                
            return Response(data={"message":"order success"})
        
