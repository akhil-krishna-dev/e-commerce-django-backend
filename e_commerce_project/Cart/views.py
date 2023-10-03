from django.shortcuts import render,redirect
from Home.models import ProductVariant
from .models import Cart
from Orders.models import OrderAddress
from django.contrib.auth.decorators import login_required



@login_required
def cart(request):
    total_price=0
    total_quantity=0
    orginal_total=0
    discount_price=0
    total_items=0
    cart=None



    try:
        cart = Cart.objects.filter(user=request.user).select_related(
            'user',
            'product_variant',
            'product_variant__product_color_variant',
            'product_variant__product_color_variant__product',
            'product_variant__product_color_variant__color',
            'product_variant__size',

            ).order_by('-updated')
        total_items = len(cart)
        for c in cart:
            total_price += (c.quantity * c.product_variant.selling_price())
            total_quantity += c.quantity
            orginal_total += (c.quantity * c.product_variant.orginal_price())
            discount_price += (c.quantity * c.product_variant.discount_price())
    except:
        pass

    return render(request, 'cart/cart.html', {
        'cart':cart,
        'total_price':total_price,
        'total_quantity':total_quantity,
        'orginal_price':orginal_total,
        'discount_price':discount_price,
        'total_items':total_items,
        })


@login_required
def add_to_cart(request,product_variant_id):
    product_variant = ProductVariant.objects.get(id=product_variant_id)

    try:
        cart = Cart.objects.create(user=request.user,
                                   product_variant=product_variant,
                                   quantity=1,
                                   price_while_order=product_variant.selling_price(),
                                   offer_while_order=product_variant.offer
                                   )
        cart.save()
    except:
        pass 
    return redirect('cart')

@login_required
def increament_product(request,product_variant_id):
    product_variant = ProductVariant.objects.get(id=product_variant_id)
    cart = Cart.objects.get(user=request.user,
                            product_variant=product_variant
                            )
    if cart.quantity < product_variant.stock:
        cart.quantity += 1
        cart.save()
    else:
        pass

    return redirect('cart')


@login_required
def decreament_product(request,product_variant_id):
    product_variant = ProductVariant.objects.get(id=product_variant_id)
    cart = Cart.objects.get(
        user=request.user,
        product_variant=product_variant
        )
    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()
    else:
        pass
    return redirect('cart')


@login_required
def remove_product(request,product_variant_id):
    product_variant = ProductVariant.objects.get(id=product_variant_id)
    cart = Cart.objects.get(
        user=request.user,
        product_variant = product_variant
        )
    cart.delete()
    return redirect('cart')

