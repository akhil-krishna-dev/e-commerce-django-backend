from django.shortcuts import render,redirect
from . forms import CustomUserCreationForm



def registration(request):
    user_form = CustomUserCreationForm()
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            print(user_form, "registration success")
            return redirect('register')
        
    return render(request, 'accounts/registration.html',{'form':user_form})
