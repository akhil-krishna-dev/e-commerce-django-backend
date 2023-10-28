from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator



class Brand(models.Model):
    name = models.CharField(unique=True, blank=False, null=False, max_length=50)
    icon = models.ImageField(blank=True, null=True, upload_to='brand/images')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to='category/images', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True,help_text='Not required.only if the brand has')
    description = models.TextField(blank=True, null=True)
    image_main = models.ImageField(upload_to='product/main/images',blank=False,null=False)
    available = models.BooleanField(default=True)
    orginal_price = models.PositiveIntegerField(blank=True, null=True)
    search_keywords = models.CharField(max_length=150, blank=True, null=True, help_text='Not required. Only for users to search for products on the website.')

    def __str__(self):
        return self.name
       




class Colors(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

class ProductColorVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, blank=True, null=True, default=1, help_text='if no color then leave it')
    image1 = models.ImageField(upload_to='product/images',blank=True,null=True)
    image2 = models.ImageField(upload_to='product/images',blank=True,null=True)
    image3 = models.ImageField(upload_to='product/images',blank=True,null=True)
    image4 = models.ImageField(upload_to='product/images',blank=True,null=True)
    image5 = models.ImageField(upload_to='product/images',blank=True,null=True)
    image6 = models.ImageField(upload_to='product/images',blank=True,null=True)
    image7 = models.ImageField(upload_to='product/images',blank=True,null=True)


    def __str__(self):
        if self.color == None:
            return self.product.name
        else:
            return self.product.name + " " + self.color.name
    


class ProductVariant(models.Model):
    product_color_variant = models.ForeignKey(ProductColorVariant, blank=True, null=True, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, blank=True, null=True, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(blank=False, null=False)
    stock = models.PositiveSmallIntegerField(blank=True, null=True)
    offer = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MaxValueValidator(100)], help_text='offer %')
    
    
    def orginal_price(self):
        return self.product_color_variant.product.orginal_price

    def selling_price(self):
        return self.product_color_variant.product.orginal_price - self.product_color_variant.product.orginal_price//100*self.offer
    
    def discount_price(self):
        return self.product_color_variant.product.orginal_price//100 * self.offer


    def get_url(self):
        return reverse('product_details', args = [ 
            self.product_color_variant.product.category.slug, 
            self.product_color_variant.product.slug, 
            self.product_color_variant.color.name, 
            self.size.name
        ])
        
    

    def __str__(self):
        if self.product_color_variant.color == None:
            return self.product_color_variant.product.name +" ("+  self.size.name+")"
        else:
            return self.product_color_variant.product.name +" ("+ self.product_color_variant.color.name +", "+ self.size.name+")"
            



    
