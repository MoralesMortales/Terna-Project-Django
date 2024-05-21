from django.shortcuts import get_object_or_404, redirect, render #type:ignore
from django.views.generic import TemplateView #type:ignore
from django.conf import settings #type:ignore
from .forms import CarreraForm, EstudianteForm, SecretarioForm #type:ignore
from django.contrib.auth.models import Group #type:ignore
from .models import Carrera, Estudiante, Secretario #type:ignore
from django.contrib.auth.models import User #type:ignore
from django.contrib import messages #type:ignore
from django.contrib.auth import logout, login, authenticate  #type:ignore


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

        # Autenticar al usuario usando el email como username
        myuser = authenticate(request, username=email, password=password)

        if myuser is not None:
            login(request, myuser)

            # Verificar si el usuario es Estudiante
            try:
                estudiante = Estudiante.objects.get(email=email)
                return render(request, "menu.html", {'theusername': myuser.first_name, 'est': estudiante})
            except Estudiante.DoesNotExist:
                pass

            # Verificar si el usuario es Secretario
            try:
                secretario = Secretario.objects.get(email=email)
                return render(request, "menu_secretaria.html", {'theusername': myuser.first_name, 'theuser': secretario})
            except Secretario.DoesNotExist:
                pass

            # Si no es ni Estudiante ni Secretario
            messages.error(request, 'Tipo de usuario no reconocido')
            return redirect('login')  # Redirigir en lugar de renderizar para evitar el repost de formularios

        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
            return redirect('login')

    return render(request, "login.html")

def logOut(request):
    if request.method=="POST":   
        logout(request)
        return render(request,"menu.html") 
    return render(request,"signout.html")

def signup_S(request):
    if request.method == 'POST':
        form = SecretarioForm(request.POST)
        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            secretario = form.save(commit=False)
            secretario.user = user
            secretario.save()

            # Log in the user
            login(request, user)
            return redirect('Login') 
    else:
        form = SecretarioForm()

    return render(request, 'signup_S.html', {'form': form})

def signUp(request):
    carreras = Carrera.objects.all()
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            # Create the Estudiante instance
            estudiante = form.save(commit=False)
            estudiante.user = user
            estudiante.save()

            # Log in the user
            login(request, user)
            return redirect('Login') 
    else:
        form = EstudianteForm()

    return render(request, 'signup.html', {'form': form, 'carreras': carreras})

"""
def signUp(request):
    if request.method == "POST":
        form = EstudianteForm(request.POST)
        password = request.POST['thepassword']
        password_conf = request.POST['password_conf']
        
        if form.is_valid() and password == password_conf:
            form.save()
            the_user_name = request.POST['the_user_name']
            pname = request.POST['father_lastname']
            mname = request.POST['mother_lastname']
            theemail = request.POST['email']
            cedula = request.POST['the_cedula']
            fnaci = request.POST['fnaci']
            tlfn = request.POST['tlfn']
            sexo = request.POST['sexo']
            carrera_id = request.POST.get('carrera')  # Use carrera_id instead of carrera_views
            carrera_views = get_object_or_404(Carrera, pk=carrera_id)

            # Create a new User instance
            myuser = User.objects.create_user(username=the_user_name, email=theemail, password=password)

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
            if password != password_conf:
                messages.error(request, "Passwords do not match")
            else:
                messages.error(request, "Form is invalid")

    carreras = Carrera.objects.all()
    form = EstudianteForm()

    return render(request, 'signup.html', {'form': form, 'carreras': carreras})
"""
def menuDefaultPage(request):
    context = {}
    if request.user.is_authenticated:
        email = request.user.email
        estudiante = Estudiante.objects.get(pk=email)
        context['est'] = estudiante
        context['imagenes'] = imagenes
        return render(request, "menu.html", context)
    return render(request, "menu.html")

def ugmaPage(request):
    return render(request, "ugmaPage.html")
