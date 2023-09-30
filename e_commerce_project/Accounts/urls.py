from django.urls import path
from . import views



urlpatterns = [
    path('',views.registration, name='register'),
    path('dashbord',views.user_dashbord, name='dashbord'),
]