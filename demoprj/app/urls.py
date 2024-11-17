from django.urls import path
from . import views

urlpatterns=[
    path('',views.e_shop_login),
    path('home',views.shop_home),
    path('logout',views.e_shop_logout),
    path('register',views.register),

]