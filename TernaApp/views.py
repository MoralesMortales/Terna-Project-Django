from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.conf import settings

from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group

from .models import Estudiante, Materia, Matricula

from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import logout, login, authenticate


from django.core.mail import send_mail


# Create your views here.


class BasePage(TemplateView):
    template_name = "base.html"

class FormularioEmail(TemplateView):
    template_name = "formularioContacto.html"

def logIn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
    
        myuser = authenticate(username = username, password = password)
        
        if myuser is not None:
            login(request,myuser)
            return render(request,"menu.html", {'username':username})
            
        else:
            messages.error(request, 'Wrong username or password')
            return render(request,"login.html")
            
    return render(request,"login.html")

def logOut(request):
    if request.method=="POST":   
        logout(request)
        return render(request,"menu.html")
        
    
    return render(request,"signout.html")

def signUp(request):
    
    if request.method == "POST":
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_conf = request.POST['password_conf']
        cedula = request.POST['cedula']
        carrera_id = request.POST['idcarrera'] #esto debe ser fk 
        
        if password == password_conf:
            
            myuser = User.objects.create_user(username, email, password)
            estudiante = Estudiante.objects.create(cedula=cedula,carrera_id=carrera_id)
            estudiante.user = myuser 
            myuser.username = username
            myuser.email = email
            
            
            myuser.save()
            
            messages.success(request, "Congrats, you have signed up")
            
            return redirect("Login")
        
        else:
          messages.error(request, 'Passwords do not match')
          return render(request,'signup.html')
    return render(request,"signup.html")

def menuDefaultPage(request):
    return render(request, "menu.html")

