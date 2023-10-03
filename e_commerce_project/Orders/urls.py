from django.urls import path
from . import views


urlpatterns = [
    path('order-confirm/',views.order_confirm, name='order-confirm'),
]