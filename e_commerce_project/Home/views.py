from django.shortcuts import render,redirect
from . models import Category,ProductVariant
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.db.models import Q


def index(request,category_slug = None):
    
    categories = Category.objects.all()

    products = None

    query_set = None
    if 'search-products' in request.GET:
        query_set = request.GET.get('search-products')
        products = ProductVariant.objects.all().filter(Q(
            product_color_variant__product__name__icontains = query_set)|
            Q(product_color_variant__product__description__icontains=query_set)|
            Q(product_color_variant__product__category__name__icontains = query_set))
    
    else:


        if category_slug:
            products = ProductVariant.objects.filter(
                product_color_variant__product__category__slug= category_slug,
                product_color_variant__product__available = True
                ).select_related(
                    'product_color_variant__product__category',
                    'product_color_variant__product__brand',
                    'product_color_variant__product',
                    'product_color_variant__color',
                    'size'
                    )

        else:
            products = ProductVariant.objects.all().filter(product_color_variant__product__available = True).select_related(
                'product_color_variant__product__category',
                'product_color_variant__product__brand',
                'product_color_variant__product',
                'product_color_variant__color',
                'size')
            
    num_of_products = len(products)
    
    paginator = Paginator(products, 16)

    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    try:
        products_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products_page = paginator.page(paginator.num_pages)


    return render(request, 'home/index.html', {
        'category':categories, 
        'product':products_page,
        'query_set':query_set,
        'num_of_products':num_of_products
        })


# all products showing also category based showing function end |||||




def product_detail(request, category_slug, product_slug, color, variant):
    try:
        product = ProductVariant.objects.get(
            product_color_variant__product__category__slug = category_slug, 
            product_color_variant__product__slug = product_slug,
            product_color_variant__color__name =color,
            size__name = variant
        )
    except Exception as e:
        raise e
    
    try:
        product_color_variant = ProductVariant.objects.filter(
            product_color_variant__product__slug=product_slug, size__name = variant
            ).select_related(
                'product_color_variant__product__category',
                'product_color_variant__product__brand',
                'product_color_variant__product',
                'product_color_variant__color',
                'product_color_variant',
                'size'
                )
    except Exception as pcv:
        raise pcv
    
    try:
        product_size_variant = ProductVariant.objects.filter(
            product_color_variant__product__slug=product_slug, 
            product_color_variant__color__name=color
            ).select_related(
                'product_color_variant__product__category',
                'product_color_variant__product__brand',
                'product_color_variant__product',
                'product_color_variant__color',
                'product_color_variant',
                'size'
            ).order_by('size')
    except Exception as psv:
        raise psv
    
    
    
    return render(request, 'home/product_details.html', {

        'product':product, 
        'product_color_variant':product_color_variant, 
        'product_size_variant':product_size_variant

        })


# product details page end |||||||



# product search start >>>>>

def product_search(request):
    return render(request, 'home/search.html')


