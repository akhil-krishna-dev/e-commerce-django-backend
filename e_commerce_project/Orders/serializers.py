from rest_framework import serializers
from .models import Orders,OrderAddress


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
        depth = 4


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = '__all__'
        depth = 1
        