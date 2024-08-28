from django.db import models
from Accounts.models import CustomUser
from Home.models import ProductVariant
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class OrderAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=False, blank=False)
    mobile = models.CharField(max_length=12,null=False, blank=False)
    pincode = models.CharField(max_length=6, null=False, blank=False)
    locality = models.CharField(max_length=60, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    city_district_town = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=20, null=False, blank=False)
    landmark = models.CharField(max_length=100, null=False, blank=False)

    
    def __str__(self):
        return self.full_name + " " + self.mobile



PAYMENT_MODE_CHOICES = (
    ('Cash On Delivery','Cash On Delivery'),
    ('RazorPay','RazorPay'),

)

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price_paid = models.PositiveIntegerField()
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODE_CHOICES)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return  " | Payment mode : "+ self.payment_mode + " | Order ID : "+ str(self.razorpay_order_id)


STATUS_CHOICES = (
    ('Cancelled','Cancelled'),
    ('Pending','Pending'),
    ('Packed','Packed'),
    ('Shipped','Shipped'),
    ('Out For Delivery','Out For Delivery'),
    ('Delivered','Delivered')
)



class Orders(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_address = models.ForeignKey(OrderAddress, on_delete=models.DO_NOTHING)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.DO_NOTHING)
    price_was = models.PositiveIntegerField(null=False, blank=False)
    quantiy_was = models.PositiveSmallIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=150, default=uuid.uuid4, unique=True,editable=False)
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.user.email +" | "+ self.product_variant.product_color_variant.product.name +" ("+self.product_variant.product_color_variant.color.name+", "+self.product_variant.size.name+")"


@receiver(post_save, sender=Orders)
def order_model_status(sender, instance, create=None, **kwrgs):

    if create:
        pass
    else:
        group_name = f"order_updates_{instance.user.id}"
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,  
            {
                "type": "send_update_message",
                "message": instance.status
            }
        )

