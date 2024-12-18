from django.urls import path
from . import views

urlpatterns=[
    path('',views.e_shop_login),
    
    #--------------------------admin---------------------
    path('home',views.shop_home),
    path('logout',views.e_shop_logout),
    path('add',views.addproduct),
    path('editproduct/<pid>',views.editproduct),
    path('deleteproduct/<pid>',views.deleteproduct),
    path('view_bookings',views.view_bookings),




    # --------------------------user------------------
    path('register',views.register),
    path('user_home',views.user_home),
    path('product_view/<pid>',views.product_view),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
    path('qty_in/<cid>',views.qty_in),
    path('qty_dec/<cid>',views.qty_dec),
    path('cart_pro_buy/<cid>',views.cart_pro_buy),
    path('bookings',views.bookings),
    path('pro_buy/<pid>',views.pro_buy),
]