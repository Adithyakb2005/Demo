from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Product
# Create your views here.
def e_shop_login(req):
    if req.method=='POST':
        username=req.POST['username']
        password=req.POST['password']
        data=authenticate(username=username,password=password)
        if data:
            login(req,data)
            return redirect(shop_home)
        else:
            messages.warning(req, "Invalid username or password.")
            return redirect(e_shop_login)
    else:
        return render(req,'login.html')

def e_shop_logout(req):
    logout(req)
    req.session.flush()
    return redirect(e_shop_login)
def shop_home(req):
    return render(req,'shop/home.html')
def addproduct(req):
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            descrip=req.POST['descrip']
            price=req.POST['price']
            stock=req.POST['stock']
            file=req.FILES['img']
            data=Product.objects.create(pid=pid,name=name,dis=descrip,price=price,stock=stock,img=file)
            data.save()
            return redirect(shop_home)
        else:
            return render(req,'shop/addproduct.html')
    else:
        return redirect(e_shop_login)
# def register(req):
#     return render(req,'register.html')