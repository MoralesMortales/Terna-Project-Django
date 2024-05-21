from django.shortcuts import get_object_or_404, redirect, render #type:ignore
from django.views.generic import TemplateView #type:ignore
from django.conf import settings #type:ignore
from django.core.exceptions import ObjectDoesNotExist
from .forms import CarreraForm, EstudianteForm, SecretarioForm, NotaEstudianteForm, EditarNotaEstudianteForm #type:ignore
from django.contrib.auth.models import Group #type:ignore
from .models import Carrera, Estudiante, Secretario, NotaEstudiante #type:ignore
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
            return redirect('Login')  # Redirigir en lugar de renderizar para evitar el repost de formularios

        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
            return redirect('Login')

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

def menuDefaultPage(request):
    if request.user.is_authenticated:
        try:
            estudiante = Estudiante.objects.get(email=request.user.email)
            return render(request, 'menu.html', {'estudiante': estudiante})
        except ObjectDoesNotExist:
            # Handle case where no Estudiante object exists for the user's email
            return render(request, 'menu.html', {'error_message': 'No Estudiante object found for this email'})
    else:
        return render(request, 'menu.html')
def ugmaPage(request):
    return render(request, "ugmaPage.html")

def gestionar_notas(request, estudiante_id):
    try:
        nota_estudiante = NotaEstudiante.objects.get(estudiante_id=estudiante_id)
    except NotaEstudiante.DoesNotExist:
        nota_estudiante = None

    if request.method == 'POST':
        form = NotaEstudianteForm(request.POST, instance=nota_estudiante)
        if form.is_valid():
            form.save()
            return redirect('menuDefault')  # Redirige a una página de éxito o a la vista deseada
    else:
        form = NotaEstudianteForm(instance=nota_estudiante)
    
    return render(request, 'notas.html', {'form': form})


def listar_notas(request):
    notas = NotaEstudiante.objects.select_related('estudiante').all()
    return render(request, 'ver_notas.html', {'notas': notas})

def lista_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    print(estudiantes)  # Add this line
    return render(request, 'lista_est.html', {'estudiantes': estudiantes})
def editar_notas_estudiante(request, email):
    estudiante = get_object_or_404(Estudiante, email=email)
    form = EditarNotaEstudianteForm(request.POST or None, instance=estudiante)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('menuDefault')
    return render(request, 'notas.html', {'form': form, 'estudiante': estudiante})
