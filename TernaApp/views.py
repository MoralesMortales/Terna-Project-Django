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
    if request.method == 'POST':
        form = ImagenForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar los datos de la imagen en la tabla ternaapp_publicaciones
            nueva_publicacion = publicaciones()
            nueva_publicacion.nombre = form.cleaned_data['nombre']
            nueva_publicacion.description = form.cleaned_data['description']
            nueva_publicacion.imagen = form.cleaned_data['imagen']
            nueva_publicacion.save()
            
            # Redireccionar a la vista correcta
            return redirect('menuDefault')
    else:
        form = ImagenForm()
    return render(request, 'createNew.html', {'form': form})


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
            
            estudiante = Estudiante.objects.get(email=email)
            return render(request,"menu.html", {'theusername':myuser.first_name,'est': estudiante})
            
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
        carrera_id = request.POST.get('carrera')  # Use carrera_id instead of carrera_views
        carrera_views = get_object_or_404(Carrera, pk=carrera_id)
        
        # Create a new User instance
        myuser = User.objects.create_user(username=theemail, email=theemail, password=password)
        
        # Create an associated Estudiante instance and set user_id
        estudiante = Estudiante.objects.create(
            nombre=the_user_name, 
            apellidoPaterno=pname, 
            email=theemail, 
            sexo=sexo, 
            apellidoMaterno=mname, 
            cedula=cedula,
            fechaNacimiento=fnaci, 
            telefono=tlfn, 
            carrera=carrera_views,
            user=myuser
        )
        
        messages.success(request, "Congrats, you have signed up")
        return redirect("Login")
    else:
        form = CarreraForm()
        messages.error(request, 'Something went wrong')
    
    carreras = Carrera.objects.all()
    
    return render(request, 'signup.html', {'form': form, 'carreras': carreras})
def menuDefaultPage(request):
    context = {}
    if request.user.is_authenticated:
        imagenes = Imagen.objects.all()
        email = request.user.email
        estudiante = Estudiante.objects.get(pk=email)
        context['est'] = estudiante
        context['imagenes'] = imagenes
        return render(request, "menu.html", context)
    return render(request, "menu.html")

def ugmaPage(request):
    return render(request, "ugmaPage.html")
