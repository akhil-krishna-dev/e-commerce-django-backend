from django.shortcuts import render,redirect
from . forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import login

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
