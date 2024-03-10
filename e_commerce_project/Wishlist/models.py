from django.db import models
from Accounts.models import CustomUser
from Home.models import ProductVariant
from django.shortcuts import redirect


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.id) +" " + str(self.user)+" "+ str(self.product_variant)
    
    def get_url(self):
        return redirect('dashbord', args=[self.pk])
    
    