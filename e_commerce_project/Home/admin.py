from django.contrib import admin
from . models import Category,Brand,Product,Colors,Size,ProductColorVariant,ProductVariant



class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name','image']
admin.site.register(Category,CategoryAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name','icon']
admin.site.register(Brand,BrandAdmin)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name','category','brand','image_main']
admin.site.register(Product,ProductAdmin)



admin.site.register([Colors,Size])


class AdminProductColorVariant(admin.ModelAdmin):
    list_display = ['product', 'color']
admin.site.register(ProductColorVariant)




class AdminProductVariant(admin.ModelAdmin):
    list_display = ['product_color_variant','orginal_price','offer','selling_price','size','stock']
admin.site.register(ProductVariant,AdminProductVariant)