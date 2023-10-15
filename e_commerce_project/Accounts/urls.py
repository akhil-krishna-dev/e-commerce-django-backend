from django.urls import path
from . import views



urlpatterns = [
    path('',views.registration, name='register'),
    path('dashbord/',views.user_dashbord, name='dashbord'),
    path('profile-pic',views.upload_profile_pic, name='profile-pic-upload'),
]