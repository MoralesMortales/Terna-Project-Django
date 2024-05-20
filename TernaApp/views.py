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

# Create your views here.


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
        
        password = request.POST.get('thepassword')
        password_conf = request.POST.get('password_conf')

        if form.is_valid():
            if password == password_conf:
                try:
                    the_user_name = request.POST.get('nombre')
                    lastname = request.POST.get('apellido')
                    theemail = request.POST.get('email')
                    cedula = request.POST.get('the_cedula')
                    fnaci = request.POST.get('fnaci')
                    tlfn = request.POST.get('tlfn')
                    sexo = request.POST.get('sexo')
                    
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

                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
            else:
                messages.error(request, "Passwords do not match")
        else:
            messages.error(request, "Form is invalid")

    else:
        form = SecretarioForm()

    return render(request, 'signup_S.html', {'form': form})

def signUp(request):
    if request.method == "POST":
        form = EstudianteForm(request.POST)
        
        if form.is_valid():
            form.save()
            password = request.POST['thepassword']
            password_conf = request.POST['password_conf']
            if password != password_conf:
                messages.error(request, "Las contraseñas no coinciden")
                return redirect('signup')
            the_user_name = request.POST['the_user_name']
            pname = request.POST['father_lastname']
            mname = request.POST['mother_lastname']
            theemail = request.POST['email']
            cedula = request.POST['the_cedula']
            fnaci = request.POST['fnaci']
            tlfn = request.POST['tlfn']
            sexo = request.POST['sexo']
            carrera_id = request.POST.get('carrera')
            carrera_views = get_object_or_404(Carrera, pk=carrera_id)

            myuser = User.objects.create_user(username=the_user_name, email=theemail, password=password)
            Estudiante.objects.create(
                nombre=the_user_name, 
                apellidoPaterno=pname, 
                apellidoMaterno=mname,
                email=theemail, 
                sexo=sexo, 
                cedula=cedula,
                fechaNacimiento=fnaci, 
                telefono=tlfn, 
                carrera=carrera_views,
                user=myuser
            )
            messages.success(request, "Congrats, you have signed up")
            return redirect("Login")
        else:
            messages.error(request, "Form is invalid")
    
    carreras = Carrera.objects.all()
    form = EstudianteForm()
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
