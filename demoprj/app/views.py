from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Product
import os
# Create your views here.
def e_shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
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

def addproducts(req) :
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            pname=req.POST['name']
            des=req.POST['descrip']
            pprice=req.POST['price']
            oprice=req.POST['off_price']
            pstock=req.POST['stock']
            file=req.FILES['img'] #to get the img from html page we  are using file method instead of post and adding enctype in html page

            data=Product.objects.create(pid=pid,name=pname,des=des,price=pprice,offer_price=oprice,stock=pstock,img=file)
            data.save()
            return redirect(shop_home)
        else:
            return render(req,'shop/add_products.html')
    else:
        return redirect(e_shop_login)    
    
def editproduct(req,pid) :
        if req.method=='POST':
            proid=req.POST['proid']
            pname=req.POST['name']
            des=req.POST['descrip']
            pprice=req.POST['price']
            oprice=req.POST['off_price']
            pstock=req.POST['stock']
            file=req.FILES.get('img')
            if file:
                Product.objects.filter(pk=pid).update(pid=proid,name=pname,des=des,price=pprice,offer_price=oprice,stock=pstock,img=file)
                data=Product.objects.get(pk=pid)
                data.img=file
                data.save()
            else:  
                Product.objects.filter(pk=pid).update(pid=pid,name=pname,des=des,price=pprice,offer_price=oprice,stock=pstock,img=file)
            return redirect(shop_home)
        else:
            data=Product.objects.get(pk=pid)
            return render(req,'shop/edit_product.html',{'data':data})

def deleteproduct(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)
# def register(req):
#     return render(req,'register.html')