from django.shortcuts import get_object_or_404, redirect, render #type:ignore
from django.views.generic import TemplateView #type:ignore
from django.conf import settings #type:ignore
from .forms import CarreraForm #type:ignore
from django.contrib.auth.models import Group #type:ignore
from .models import Carrera, Estudiante #type:ignore
from django.contrib.auth.models import User #type:ignore
from django.contrib import messages #type:ignore
from django.contrib.auth import logout, login, authenticate  #type:ignore
from django.core.mail import send_mail #type:ignore

def UgmaSite(request):
    return render(request, "ugmaPage.html")

def createNew(request):
    return render(request, "createNew.html")


# Create your views here.


class BasePage(TemplateView):
    template_name = "base.html"

class FormularioEmail(TemplateView):
    template_name = "formularioContacto.html"

def logIn(request):
    if request.method == "POST":
        email = request.POST['theemail']
        password = request.POST['password']
    
        myuser = authenticate(request, username = email, password = password)
        
        if myuser is not None:
            login(request,myuser)
            return render(request,"menu.html", {'theusername':myuser.first_name})
            
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
    
    """ estudiante = Estudiante.objects.first() """
    
    if request.method == "POST":
        form = CarreraForm(request.POST)
        if form.is_valid():
            form.save()
        the_user_name = request.POST['the_user_name']
        pname = request.POST['father_lastname']
        mname = request.POST['mother_lastname']
        theemail = request.POST['email']
        password = request.POST['thepassword']
        password_conf = request.POST['password_conf']
        cedula = request.POST['the_cedula']
        fnaci = request.POST['fnaci']
        tlfn = request.POST['tlfn']
        sexo = request.POST['sexo']
        carrera_views= request.POST.get('carrera')
        carrera_views = get_object_or_404(Carrera, pk=carrera_views)
        
        myuser = User.objects.create_user(first_name = the_user_name, email =  theemail, last_name = pname, username = theemail, password = password)
        
        estudiante = Estudiante.objects.create(nombre=the_user_name, apellidoPaterno = pname ,email =  theemail, sexo = sexo, apellidoMaterno = mname, cedula=cedula,fechaNacimiento=fnaci, telefono=tlfn, carrera=carrera_views)
        
        estudiante.user = myuser 
        
        """ myuser.username = theusername
        myuser.email = email """
        
        myuser.save() 
        
        messages.success(request, "Congrats, you have signed up")
        
        return redirect("Login")
        
    else:
        form = CarreraForm()
        messages.error(request, 'Something went wrong')
        
    carreras = Carrera.objects.all()
    
    return render(request, 'signup.html', {'form': form, 'carreras': carreras, 'estudiante': Estudiante})

def menuDefaultPage(request):
    context = {'the_user_name': request.user.username}
    return render(request, "menu.html", context)
