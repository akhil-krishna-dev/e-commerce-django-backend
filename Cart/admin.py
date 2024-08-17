from django.contrib import admin
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ['product_variant', 'user', 'quantity', 'updated']
admin.site.register(Cart,CartAdmin)
