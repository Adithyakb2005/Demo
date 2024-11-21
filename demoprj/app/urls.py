from django.urls import path
from . import views

urlpatterns=[
    path('',views.e_shop_login),
    path('home',views.shop_home),
    path('logout',views.e_shop_logout),
    path('add',views.addproduct),
    path('editproduct/<pid>',views.editproduct),
    path('deleteproduct/<pid>',views.deleteproduct),
    path('register',views.register),
    path('user_home',views.user_home),
    path('product_view/<pid>',views.product_view),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart)

]