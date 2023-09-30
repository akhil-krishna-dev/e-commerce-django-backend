from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart, name='cart'),
    path('add/<int:product_variant_id>/',views.add_to_cart, name='add_to_cart'),
    path('increament/<int:product_variant_id>/',views.increament_product, name='increament'),
    path('decreament/<int:product_variant_id>/',views.decreament_product, name='decreament'),
    path('remove/<int:product_variant_id>/',views.remove_product, name='remove')

]