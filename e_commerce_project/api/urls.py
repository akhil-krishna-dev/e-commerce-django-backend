from django.urls import path,include
from rest_framework import routers
from Home.api_views import *
from Wishlist.api_view import WishlistView,AddToWishlistView,delete_wishlist
from Orders.api_views import *
from Accounts.api_view import (UserProfileView,
    UserRegisterView,UserLoginView,
    UserLogOut,
    UserPasswordForgotView,
    PasswordResetView,
    EmailVerificationView)
from Cart.api_views import CartApiView,AddCartApiView,increament_cart,decreament_cart,delete_cart
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)




router = routers.DefaultRouter()
router.register(r'product-variants', ProductVariantView, 'product-variant')
router.register(r'categories',CategoryView, 'category')
router.register(r'orders',OrderView, 'order')
router.register(r'order-address',OrderAddressView, 'user-address')
router.register(r'cart/add-cart',AddCartApiView,'added-cart')
router.register(r'product/reviews',ProductReviewView, 'review')
router.register(r'product/recent-products', RecentViewedProductsView, 'recent-product')

urlpatterns = router.urls

urlpatterns = [
    path('',include(router.urls)),
    path('product/description/', ProductDescriptionView.as_view(), name='product-description'),
    path('user/profile/',UserProfileView.as_view(), name='user-profile'),
    path('user/registration/',UserRegisterView.as_view(), name='user-register'),
    path('user/logout/',UserLogOut.as_view(), name='user-logout'),
    path('cart/',CartApiView.as_view(), name='cart-list'),
    path('cart/in-cart/',CartApiView.in_cart, name='in-cart'),
    path('wishlist/',WishlistView.as_view(),name='wishlist-view'),
    path('wishlist/add/',AddToWishlistView.as_view(),name='wishlist-add'),
    path('wishlist/in-wishlist/',WishlistView.in_wishlist,name='in-wishlist'),
    path('cart/increament-qty/',increament_cart, name='increament-qty'),
    path('cart/decreament-qty/',decreament_cart, name='decreament-qty'),
    path('cart/delete-cart/',delete_cart, name='delete-cart'),
    path('wishlist/delete/',delete_wishlist, name='wishlist-delete'),
    path('cart/count/',CartApiView.cart_count, name='cart-count'),
    path('order-confirm/',OrderConfirmView.as_view(), name='order-confirm'),
    path('order/cash-on-delivery/', CashOnDeliveryView.as_view(), name='cash-on-delivery'),
    path('razorpay-payment-request/' ,initiate_payment, name='razorpay-payment'),
    path('razorpay-payment-fail/',razorpay_payment_failure, name='razorpay-fail'),
    path('user/login/token/',UserLoginView.as_view(),name='token'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/password-forgot/', UserPasswordForgotView.as_view(),name='forgot-password'),
    path('user/password-reset/',PasswordResetView.as_view(), name='reset-password'),
    path('user/activate-email/<str:uidb64>/<str:token>/', EmailVerificationView.as_view(), name='email-verify'),
    path('product/reveiw-submit/', product_review_save, name='reveiw-save'),
    
]