from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Cart.models import Cart
from .models import OrderAddress

@login_required
def order_confirm(request):
    orginal_total = 0
    discount_price = 0
    total_price = 0
    total_items = 0

    cart = Cart.objects.filter(user=request.user)
    total_items = len(cart)
    for c in cart:
        orginal_total += (c.quantity * c.product_variant.orginal_price())
        discount_price += (c.quantity * c.product_variant.discount_price())
        total_price += (c.quantity * c.product_variant.selling_price())


# order address saving method

    if request.method == 'POST':
        order_address_id = request.POST['address-id']
        name = request.POST['yourname']
        mobile = request.POST['phone']
        pin = request.POST['pincode']
        locality = request.POST['locality']
        address = request.POST['address']
        district = request.POST['district']
        state = request.POST['state']
        landmark = request.POST['landmark']


        if OrderAddress.objects.filter(id=order_address_id).exists:
            address = OrderAddress.objects.filter(id=order_address_id).update(
            user = request.user,
            full_name = name,
            mobile = mobile,
            pincode = pin,
            locality = locality,
            address = address,
            city_district_town = district,
            state = state,
            landmark = landmark 
            )
            return redirect('order-confirm')     
        else:
            address = OrderAddress.objects.create(
            user = request.user,
            full_name = name,
            mobile = mobile,
            pincode = pin,
            locality = locality,
            address = address,
            city_district_town = district,
            state = state,
            landmark = landmark 
            )
            address.save()
            return redirect('order-confirm')
# order address saving method ends

   

# all the order address fetching
    order_address = OrderAddress.objects.filter(user=request.user)


    return render(request, 'order/order-confirm.html', {
        'orginal_price':orginal_total,
        'discount_price':discount_price,
        'total_price':total_price,
        'total_items':total_items,
        'order_address':order_address
    })


# order address save

