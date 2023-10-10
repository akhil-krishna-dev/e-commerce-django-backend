from django.contrib import admin
from .models import OrderAddress,Payment,Orders


admin.site.register(OrderAddress)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','order_address','product_variant','price_was','quantiy_was','status','payment']
admin.site.register(Orders,OrderAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','payment_mode','razorpay_order_id','price_paid']
admin.site.register(Payment,PaymentAdmin)