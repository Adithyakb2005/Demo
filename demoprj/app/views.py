from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User
# Create your views here.
def e_shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        username=req.POST['username']
        password=req.POST['password']
        data=authenticate(username=username,password=password)
        if data:
            login(req,data)
            if data.is_superuser:
                req.session['shop']=username #create
                return redirect(shop_home)
            else:
                req.session['user']=username 
                return redirect(user_home)
        else:
            messages.warning(req, "Invalid username or password.")
            return redirect(e_shop_login)
    else:
        return render(req,'login.html')

def e_shop_logout(req):
    logout(req)
    req.session.flush()
    return redirect(e_shop_login)
#---------------------admin------------------------

def shop_home(req):
    if 'shop' in req.session:
        data=Product.objects.all()
        return render(req,'shop/home.html',{'Products':data})
    else:
        return redirect(e_shop_login)

def addproduct(req) :
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            dis=req.POST['descrip']
            price=req.POST['price']
            stock=req.POST['stock']
            file=req.FILES['img'] #to get the img from html page we  are using file method instead of post and adding enctype in html page

            data=Product.objects.create(pid=pid,name=name,dis=dis,price=price,stock=stock,img=file)
            data.save()
            return redirect(shop_home)
        else:
            return render(req,'shop/addproduct.html')
    else:
        return redirect(e_shop_login)    
    
def editproduct(req,pid) :
        if req.method=='POST':
            proid=req.POST['proid']
            name=req.POST['name']
            dis=req.POST['descrip']
            price=req.POST['price']
            stock=req.POST['stock']
            file=req.FILES.get('img')
            if file:
                Product.objects.filter(pk=pid).update(pid=proid,name=name,dis=dis,price=price,stock=stock,img=file)
                data=Product.objects.get(pk=pid)
                data.img=file
                data.save()
            else:  
                Product.objects.filter(pk=pid).update(pid=pid,name=name,dis=dis,price=price,stock=stock,img=file)
            return redirect(shop_home)
        else:
            data=Product.objects.get(pk=pid)
            return render(req,'shop/edit.html',{'data':data})

def deleteproduct(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)
def view_bookings(req):
    buy=Buy.objects.all()[::-1]
    return render(req,'shop/viewbooking.html', {'buy':buy})
#--------------------------------user--------------------
def register(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['pswd']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=pswd)
            data.save()
        except:
            messages.warning(req,"email already in use")
            return redirect(register)

        return redirect(e_shop_login)
    else:
        return render(req,'user/register.html')
def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/userhome.html',{'product':data})
    else:
        return redirect(e_shop_login)

def product_view(req,pid):
       data=Product.objects.get(pk=pid)
       return render(req,'user/product_view.html',{'product':data})
    

def add_to_cart(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(user=user,product=product)
        cart.qty+=1
        cart.save()
    except:
        data=Cart.objects.create(product=product,user=user,qty=1)
        data.save()
    return  redirect(view_cart)
def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})

def qty_in(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty+=1
    data.save()
    return redirect(view_cart)
def qty_dec(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    print(data.qty)
    if data.qty==0:
        data.delete()
    return redirect(view_cart)
def cart_pro_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    product=cart.product
    user=cart.user
    qty=cart.qty
    price=product.price*qty
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)


def pro_buy(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=product.price
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)



def bookings(req):
    user=User.objects.get(username=req.session['user'])
    buy=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/booking.html',{'bookings':buy})