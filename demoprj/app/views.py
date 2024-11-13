from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
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
            messages.warning(req, "Your account expires in three days.")
            return redirect(e_shop_login)
    else:
        return render(req,'login.html')


def shop_home(req):
    return render(req,'shop\home.html')