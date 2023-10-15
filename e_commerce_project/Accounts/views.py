from django.shortcuts import render,redirect
from . forms import CustomUserCreationForm
from .models import CustomUser
from Orders.models import OrderAddress
from Wishlist.models import Wishlist
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def registration(request):
    user_form = CustomUserCreationForm()
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            user_form = CustomUserCreationForm(request.POST)
            if user_form.is_valid():
                user_form.save()

                user = auth.authenticate(email=user_form.cleaned_data['email'], password = user_form.cleaned_data['password1'])
                if user:
                    login(request, user)
                messages.success(request, "welcome "+user_form.cleaned_data['first_name'])
                return redirect('home')
        
    return render(request, 'accounts/registration.html', {'form':user_form})


# user account dashbord
@login_required()
def user_dashbord(request):
    custom_user = CustomUser.objects.get(id=request.user.id)
    order_address = OrderAddress.objects.filter(user=custom_user).select_related('user')
    wishlist = Wishlist.objects.filter(user=custom_user).select_related(
        'product_variant__product_color_variant__product__category',
        'product_variant__product_color_variant__color',
        'product_variant__size',
        'user'
    )
    
    context = {
        'user':custom_user,
        'order_address':order_address,
        'wishlist':wishlist
    }
    

    return render(request, 'accounts/dashbord.html',context)



def upload_profile_pic(request):
    
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST' :
        picture = request.FILES.get('profile-pic')
        user.profile_image.delete()
        user.profile_image = picture
        user.save()
        
        
    return redirect('dashbord')


