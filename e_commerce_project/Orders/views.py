from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Cart.models import Cart
from .models import OrderAddress,Payment,Orders
from Accounts.models import CustomUser
from django.conf import settings
import razorpay
import uuid
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt



@login_required
def order_confirm(request):
    orginal_total = 0
    discount_price = 0
    total_price = 0
    total_items = 0
    item_name = ""

    cart = Cart.objects.filter(user=request.user).select_related(
        'product_variant__product_color_variant__product__category',
        'product_variant__product_color_variant__product__brand',
        'product_variant__product_color_variant__product',
        'product_variant__product_color_variant__color',
        'product_variant__product_color_variant',
        'product_variant__size',
        'user',
        
    )
    total_items = len(cart)
    for c in cart:
        orginal_total += (c.quantity * c.product_variant.orginal_price())
        discount_price += (c.quantity * c.product_variant.discount_price())
        total_price += (c.quantity * c.product_variant.selling_price())
        item_name += c.product_variant.product_color_variant.product.name
    

    
    host = request.get_host()

# RAZORPAY SECTION
    receipt_uuid = uuid.uuid4()
    razorpay_total_price = int(total_price * 100)
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    DATA = {
        "amount": razorpay_total_price,
        "currency": "INR",
        "receipt": "rec_"+str(receipt_uuid),
    }
    razorpay_response = client.order.create(data=DATA)





# PAYPAL SECTION  
    paypal_checkout = {
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount':total_price,
        'item_name':item_name,
        'invoice':uuid.uuid4(),
        'currency_code':'USD',
        'notify_url': "http://{}{}".format(host,reverse('paypal-ipn')),
        'return_url': "http://{}{}".format(host,reverse('payment-success', kwargs={'cart_items':cart})),
        'cancel_url': "http://{}{}".format(host,reverse('payment-fail', kwargs={'cart_items_f':cart})),

    }
    paypal_payment = PayPalPaymentsForm(initial = paypal_checkout)
    


# all the order address fetching
    order_address = OrderAddress.objects.filter(user=request.user)



    context = {
        'orginal_price':orginal_total,
        'discount_price':discount_price,
        'total_price':total_price,
        'total_items':total_items,
        'order_address':order_address,
        'payment':razorpay_response,
        'paypal':paypal_payment,
        'key':settings.KEY
    }
    
    return render(request, 'order/order-confirm.html', context)





# order address saving method
@login_required
def address_creation(request):
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

        if order_address_id == "create":
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
        else:
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
                
    return redirect('order-confirm')
# order address saving method ends


@csrf_exempt
def razorpay_payment_success(request,user):
    total_price_paid = 0
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_signature = request.POST.get('razorpay_signature')
    

    order_address_id = request.POST.get('address-selected')
    if request.method == 'POST':
         
        client.utility.verify_payment_signature({
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
        })
        
        user_obj = CustomUser.objects.get(email=user)
        cart = Cart.objects.filter(user=user_obj)

        for c in cart:
            total_price_paid += (c.quantity * c.product_variant.selling_price())
            payment_obj = Payment.objects.create(
                user=user_obj,
                price_paid = total_price_paid,
                payment_mode = 'RazorPay',
                razorpay_order_id = razorpay_order_id,
                razorpay_payment_status = 'Paid',
                razorpay_payment_id = razorpay_payment_id,
                paid = True
            )
            payment_obj.save()


            order = Orders.objects.create(
                user = user_obj,
                order_address = OrderAddress.objects.get(id=str(order_address_id)),
                product_variant = c.product_variant,
                price_was = c.product_variant.selling_price(),
                quantiy_was = c.quantity,
                payment = payment_obj
            )
            order.save()
            c.delete()

        
        return redirect('razorpay-success', {'razor_order_id':razorpay_order_id})
    

    return render(request, 'payments/success_payment.html')


def paypal_payment_success(request,prod_variant_id):
    return render(request, 'payments/success_payment.html')


def paypal_payment_fail(request, prod_varian_id):
    return render(request, 'payments/failed_payment.html')




# all Orders section
def all_orders(request):
    return render(request, 'order/all_orders.html')