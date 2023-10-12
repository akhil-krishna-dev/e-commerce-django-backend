from django.contrib.auth.decorators import login_required
from Home.models import ProductVariant
from .models import Wishlist
from django.http import JsonResponse
import json


@login_required()
def add_to_wishlist(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.load(request)
        product_variant_id = (data['pid'])
        product_variant = ProductVariant.objects.get(id=product_variant_id)
        wishlist = Wishlist.objects.create(
            user = request.user,
            product_variant = product_variant
        )
        wishlist.save()
        return JsonResponse({"status":"Item added to wishlist"}, status=200)
        

    else:
        return JsonResponse({'status':"invalid access"},status=200)



