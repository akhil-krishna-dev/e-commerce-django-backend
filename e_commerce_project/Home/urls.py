from django.urls import path
from . import views



urlpatterns = [
    path('',views.index,name= 'home'),
    path('<slug:category_slug>/',views.index, name='category_view'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_details'),
]