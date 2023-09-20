from django.shortcuts import render,redirect
from . models import Category,Product,ProductColorVariant
from django.core.paginator import Paginator,EmptyPage,InvalidPage


def index(request,category_slug = None):
    
    categories = Category.objects.all()

    products = None
    if category_slug:
        products = Product.objects.filter(category__slug = category_slug)
    else:
        products = Product.objects.all()
    
    paginator = Paginator(products, 1)

    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    try:
        products_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products_page = paginator.page(paginator.num_pages)


    return render(request, 'home/index.html', {'category':categories, 'product':products_page})





def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get( category__slug = category_slug, slug = product_slug)
    except Exception as e:
        raise e
    
    try:
        product_variant = ProductColorVariant.objects.all().select_related('color')
    except Exception as pv:
        raise pv
    return render(request, 'home/product_details.html', {'product':product, 'product_variant':product_variant})



