from django.db import models
from Accounts.models import CustomUser


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