from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.conf import settings

from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from . import forms,models

from django.contrib.auth.models import User
from django.contrib import messages

from django.core.mail import send_mail
# Create your views here.


class BasePage(TemplateView):
    template_name = "base.html"

class FormularioEmail(TemplateView):
    template_name = "formularioContacto.html"

def logIn(request):
    return render(request,"login.html")

def logOut(request):
    return render(request,"logout.html")

def signUp(request):
    
    if request.method == "POST":
        
        username = request.POST['username']
        password = request.POST['password']
        password_conf = request.POST['password_conf']
        
        if password == password_conf:
              
            myuser = User.objects.create_user(username, password)
            myuser.save()
            
            messages.success(request, "Congrats, you have signed up")
            
            return redirect("Login")
        
        else:
          messages.error(request, 'Passwords do not match')
          return render(request,'signup.html')
    return render(request,"signup.html")

def menuDefaultPage(request):
    return render(request, "menu.html")