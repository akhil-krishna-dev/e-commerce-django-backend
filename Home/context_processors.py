from Cart.models import Cart
from django.core.exceptions import ObjectDoesNotExist


def cart_items(request):
    cart_count = 0
    if request.user.is_authenticated:
        if 'admin' in request.path:
            return {}
        else:
            try:
                cart = Cart.objects.filter(user=request.user)
                cart_count = len(cart)
            except ObjectDoesNotExist:
                cart_count = 0
    return dict(cart_counts=cart_count)
