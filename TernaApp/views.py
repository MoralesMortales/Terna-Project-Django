from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.conf import settings
from .forms import CarreraForm
from django.contrib.auth.models import Group
from .models import Estudiante, Carrera
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.core.mail import send_mail

def createNew(request):
    return render(request, "createNew.html")

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
        form = CarreraForm(request.POST)
        if form.is_valid():
            form.save()
        username = request.POST['username']
        pname = request.POST['pname']
        mname = request.POST['mname']
        email = request.POST['email']
        password = request.POST['password']
        password_conf = request.POST['password_conf']
        cedula = request.POST['cedula']
        fnaci = request.POST['fnaci']
        tlfn = request.POST['tlfn']
        sexo = request.POST['sexo']
        carrera_views= request.POST.get('carrera')
        carrera_views = get_object_or_404(Carrera, pk=carrera_views)
        myuser = User.objects.create_user(username, email, password)
        estudiante = Estudiante.objects.create(nombre=username,apellidoPaterno=pname,sexo = sexo,apellidoMaterno=mname,cedula=cedula,fechaNacimiento=fnaci,telefono=tlfn,carrera=carrera_views)
        estudiante.user = myuser 
        myuser.username = username
        myuser.email = email
        myuser.save() 
        messages.success(request, "Congrats, you have signed up")
        return redirect("Login")
        
    else:
        form = CarreraForm()
        messages.error(request, 'Something went wrong')
        
    carreras = Carrera.objects.all()
    return render(request, 'signup.html', {'form': form, 'carreras': carreras})

def menuDefaultPage(request):
    context = {'username': request.user.username}
    return render(request, "menu.html", context)
