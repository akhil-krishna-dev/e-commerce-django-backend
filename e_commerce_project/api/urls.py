from django.urls import path,include
from rest_framework import routers
from Home.api_views import ProductVariantView,CategoryView
from Wishlist.api_view import WishlistView
from Orders.api_views import OrderView,OrderAddressView
from Accounts.api_view import UserProfileView,UserRegisterView,UserLoginView,UserLogOut


router = routers.DefaultRouter()
router.register(r'product-variants', ProductVariantView, 'product-variant')
router.register(r'categories',CategoryView, 'category')
router.register(r'wishlists', WishlistView, 'wishlist')
router.register(r'orders',OrderView, 'order')
router.register(r'order-address',OrderAddressView, 'user-address')


urlpatterns = router.urls

urlpatterns = [
    path('',include(router.urls)),
    path('user/profile/',UserProfileView.as_view(), name='user-profile'),
    path('user/registration/',UserRegisterView.as_view(), name='user-register'),
    path('user/login/',UserLoginView.as_view(), name='user-login'),
    path('user/logout/',UserLogOut.as_view(), name='user-logout'),
]