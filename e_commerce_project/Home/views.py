from django.shortcuts import render,redirect
from . models import Category,Product,ProductColorVariant,ProductVariant
from django.core.paginator import Paginator,EmptyPage,InvalidPage


def index(request,category_slug = None):
    
    categories = Category.objects.all()

    products = None
    if category_slug:
        products = ProductVariant.objects.filter(product_color_variant__product__category__slug= category_slug)

    else:
        products = ProductVariant.objects.all()
    
    paginator = Paginator(products, 16)

    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    try:
        products_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products_page = paginator.page(paginator.num_pages)


    return render(request, 'home/index.html', {'category':categories, 'product':products_page})





def product_detail(request, category_slug, product_slug, color, variant):
    try:
        product = ProductVariant.objects.get(product_color_variant__product__category__slug = category_slug, product_color_variant__product__slug = product_slug,product_color_variant__color__name =color,size__name = variant)
    except Exception as e:
        raise e
    
    try:
        product_color_variant = ProductVariant.objects.filter(product_color_variant__product__slug=product_slug, size__name = variant).select_related('product_color_variant')
    except Exception as pcv:
        raise pcv
    
    try:
        product_size_variant = ProductVariant.objects.filter(product_color_variant__product__slug=product_slug, product_color_variant__color__name=color)
    except Exception as psv:
        raise psv
    
    
    
    return render(request, 'home/product_details.html', {'product':product, 'product_color_variant':product_color_variant, 'product_size_variant':product_size_variant})



