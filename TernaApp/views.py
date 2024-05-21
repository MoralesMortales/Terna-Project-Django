from django.shortcuts import get_object_or_404, redirect, render #type:ignore
from django.views.generic import TemplateView #type:ignore
from django.conf import settings #type:ignore
from .forms import CarreraForm, EstudianteForm, SecretarioForm #type:ignore
from django.contrib.auth.models import Group #type:ignore
from .models import Carrera, Estudiante, Secretario #type:ignore
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

class BasePage(TemplateView):
    template_name = "base.html"

class FormularioEmail(TemplateView):
    template_name = "formularioContacto.html"

def logIn(request):
    if request.method == "POST":
        email = request.POST['theemail']
        password = request.POST['password']

        myuser = authenticate(request, email=email, password=password)

        if myuser is not None:
            login(request, myuser)

            # Check if the user is an Estudiante
            try:
                estudiante = Estudiante.objects.get(email=email)
                return render(request, "menu.html", {'theusername': myuser.first_name, 'est': estudiante})
            except Estudiante.DoesNotExist:
                pass

            # Check if the user is a Secretario
            try:
                secretario = Secretario.objects.get(email=email)
                return render(request, "menu_secretaria.html", {'theusername': myuser.first_name, 'theuser': secretario})
            except Secretario.DoesNotExist:
                pass

            # If neither Estudiante nor Secretario
            messages.error(request, 'User type not recognized')
            return render(request, "login.html")

        else:
            messages.error(request, 'Wrong username or password')
            return render(request, "login.html")

    return render(request, "login.html")

def logOut(request):
    if request.method=="POST":   
        logout(request)
        return render(request,"menu.html") 
    return render(request,"signout.html")

def signup_S(request):
    if request.method == "POST":
        form = SecretarioForm(request.POST)

        if form.is_valid():
                    the_user_name = request.POST.get('nombre')
                    lastname = request.POST.get('apellido')
                    cedula = request.POST.get('the_cedula')
                    sexo = request.POST.get('sexo')
                    fnaci = request.POST.get('fnaci')
                    theemail = request.POST.get('email')
                    password = request.POST.get('thepassword')
                    password_conf = request.POST.get('password_conf')
                    tlfn = request.POST.get('tlfn')
                    
                    myuser = User.objects.create_user(username=the_user_name, email=theemail, password=password)

                    # Create Secretario instance and associate with user
                    Secretario.objects.create(
                        nombre=the_user_name,
                        apellido=lastname,
                        email=theemail,
                        sexo=sexo,
                        cedula=cedula,
                        fechaNacimiento=fnaci,
                        telefono=tlfn,
                        user=myuser
                    )

                    messages.success(request, "Congrats, you have signed up")
                    return redirect("login")

        else:
            messages.error(request, "Form is invalid")

    else:
        form = SecretarioForm()

    return render(request, 'signup_S.html', {'form': form})

def signUp(request):
    if request.method == "POST":
        form = EstudianteForm(request.POST)
        password = request.POST['thepassword']
        password_conf = request.POST['password_conf']

        if form.is_valid() and password == password_conf:
            try:
                # Extract data from the form
                the_user_name = form.cleaned_data['the_user_name']
                pname = form.cleaned_data['father_lastname']
                mname = form.cleaned_data['mother_lastname']
                theemail = form.cleaned_data['email']
                cedula = form.cleaned_data['the_cedula']
                fnaci = form.cleaned_data['fnaci']
                tlfn = form.cleaned_data['tlfn']
                sexo = form.cleaned_data['sexo']
                carrera_id = form.cleaned_data['carrera']

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
                return redirect("login")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            if password != password_conf:
                messages.error(request, "Passwords do not match")
            else:
                messages.error(request, "Form is invalid")
                print(form.errors)  # Imprimir los errores del formulario en la consola

    else:
        form = EstudianteForm()

    carreras = Carrera.objects.all()
    return render(request, 'signup.html', {'form': form, 'carreras': carreras})


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
