from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .serializers import OrderSerializer,OrderAddressSerializer,OrderConfirmSerializer
from .models import Orders,OrderAddress
from django.conf import settings
from rest_framework.response import Response
from Cart.models import Cart


class OrderView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Orders.objects.filter(user=user)



class OrderAddressView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = OrderAddressSerializer
    
    def get_queryset(self):
        user = self.request.user
        return OrderAddress.objects.filter(user=user)
    


class OrderConfirmView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = OrderConfirmSerializer


    def post(self,request):
        print("self section ",request)
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.data)



# razorpay payment handler
from django.http import JsonResponse
import razorpay
from rest_framework.decorators import api_view

@api_view(['POST'])
def initiate_payment(request):
    if request.method == 'POST':
        amount =  0
        cart = Cart.objects.filter(user=request.user)
        for c in cart:
            amount += (c.quantity * c.product_variant.selling_price())
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        
        amount *=100
        payment_data = {
            'amount': amount,
            'currency': 'INR',
            'receipt': 'order_rcptid_11',
        }

        order = client.order.create(data=payment_data)
        print('order data ',payment_data)
        return Response(data=order)

    return Response(data={'message':'method is not post'})

    