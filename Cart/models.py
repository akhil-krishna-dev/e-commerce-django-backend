from django.db import models
from Accounts.models import CustomUser
from Home.models import ProductVariant

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    price_while_order = models.PositiveIntegerField()
    offer_while_order = models.PositiveSmallIntegerField(null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product_variant.product_color_variant.product.name +" "+ self.product_variant.product_color_variant.color.name+" "+self.product_variant.size.name+" cart id("+ str(self.pk)+")"