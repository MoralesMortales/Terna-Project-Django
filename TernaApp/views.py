from datetime import date
from django.shortcuts import get_object_or_404, redirect, render #type:ignore
from django.views.generic import TemplateView #type:ignore
from django.conf import settings
from TernaApp.utils import get_serializable_messages #type:ignore
from .forms import CarreraForm, MateriasForm, ProfesorForm,EstudianteForm, SecretarioForm, AprobarProfesorForm,AprobarEstudianteForm #type:ignore
from django.contrib.auth.models import Group #type:ignore
from django.core.exceptions import ObjectDoesNotExist
from .models import Carrera, Estudiante, Secretario, NotaEstudiante, Profesor #type:ignore
from django.contrib.auth.models import User #type:ignore
from django.contrib import messages #type:ignore
from django.contrib.auth.decorators import login_required #type:ignore
from django.contrib.auth import logout, login, authenticate  #type:ignore

@login_required
def materias_asignadas(request):
    if hasattr(request.user, 'profesor'):
        profesor = request.user.profesor
        materias = Materia.objects.filter(profesor=profesor)
        return render(request, 'materias_asignadas.html', {'materias': materias})
    else:
        return redirect('home')

@login_required
def crear_materia(request):
    if hasattr(request.user, 'secretario'):
        if request.method == 'POST':
            form = MateriaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('lista_materias')
        else:
            form = MateriaForm()
        return render(request, 'crear_materia.html', {'form': form})
    else:
        return redirect('home')

def UgmaSite(request):
    return render(request, "ugmaPage.html")

def UgmaContacto(request):
    return render(request, "contactanosUgma.html")

def createNew(request):
    if request.method == 'POST':
        form = MateriasForm(request.POST)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.save()
            return redirect('menuDefault') 
         
    return render(request, 'createNew.html')
class BasePage(TemplateView):
    template_name = "base.html"

def settings_page(request):
    return render(request, "settings.html")    

def create_subject(request):
    
    return render(request, "createSubject.html")    

def logIn(request):
    if request.method == "POST":
        email = request.POST['theemail']
        password = request.POST['password']

        # Autenticar al usuario usando el email como username
        myuser = authenticate(request, username=email, password=password)

        if myuser is not None:
            # Verificar si el usuario es Estudiante
            try:
                estudiante = Estudiante.objects.get(user=myuser)
                if not estudiante.aprobado:
                    messages.error(request, 'Tu cuenta de estudiante aún no ha sido aprobada.')
                    return redirect('Login')
                login(request, myuser)
                return render(request, "menu_student.html", {'theusername': myuser.first_name, 'est': estudiante})
            except Estudiante.DoesNotExist:
                pass

            # Verificar si el usuario es Secretario
            try:
                secretario = Secretario.objects.get(user=myuser)
                login(request, myuser)
                return render(request, "menu_secretaria.html", {'theusername': myuser.first_name, 'theuser': secretario})
            except Secretario.DoesNotExist:
                pass

            # Verificar si el usuario es Profesor
            try:
                profesor = Profesor.objects.get(user=myuser)
                if not profesor.aprobado:
                    messages.error(request, 'Tu cuenta de profesor aún no ha sido aprobada.')
                    return redirect('Login')
                login(request, myuser)
                return render(request, "menu_profesor.html", {'theusername': myuser.first_name, 'profesor': profesor})
            except Profesor.DoesNotExist:
                pass

            # Si no es ni Estudiante, ni Secretario, ni Profesor
            messages.error(request, 'Tipo de usuario no reconocido')
            return redirect('Login')

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
    today = date.today().isoformat() 
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
            return redirect('Login',{'today': today}) 
    else:
        form = SecretarioForm()

    return render(request, 'signup_S.html', {
        'form': form,
        'today': today
    })

def signup_P(request):
    today = date.today().isoformat() 
    if request.method == 'POST':
        form = ProfesorForm(request.POST)

        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            profesor = form.save(commit=False)
            profesor.user = user
            profesor.save()

            # Log in the user
            login(request, user)
            return redirect('Login') 
    else:
        form = ProfesorForm()

    return render(request, 'signup_P.html', {
        'form': form,
        'today': today
        
    })

def signUp(request):
    carreras = Carrera.objects.all()
    today = date.today().isoformat() 
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

    return render(request, 'signup.html', {'form': form, 'carreras': carreras, 'today': today})

def menuDefaultPage(request):
    if hasattr(request.user, 'secretario'):
        return render(request, 'menu_secretaria.html')
    elif hasattr(request.user, 'profesor'):
        return render(request, 'menu_profesor.html')
    elif hasattr(request.user, 'estudiante'):
        return render(request, 'menu_student.html')
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

@login_required
def aprobar_estudiante(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    if request.method == "POST":
        form = AprobarEstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            return redirect('lista_estudiantes')
    else:
        form = AprobarEstudianteForm(instance=estudiante)
    return render(request, 'aprobar_estudiante.html', {'form': form})

@login_required
def aprobar_profesor(request, profesor_id):
    profesor = get_object_or_404(Profesor, id=profesor_id)
    if request.method == "POST":
        form = AprobarProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            return redirect('lista_profesores')
    else:
        form = AprobarProfesorForm(instance=profesor)
    return render(request, 'aprobar_profesor.html', {'form': form})
@login_required
def approve_users(request):
    if hasattr(request.user, 'secretario'):  # Esta línea debería ser corregida
        estudiantes_pendientes = Estudiante.objects.filter(aprobado=False)
        profesores_pendientes = Profesor.objects.filter(aprobado=False)

        if request.method == "POST":
            user_type = request.POST.get('user_type')
            user_id = request.POST.get('user_id')
            action = request.POST.get('action')
            
            try:
                if user_type == 'estudiante':
                    estudiante = Estudiante.objects.get(pk=user_id)
                    if action == 'approve':
                        estudiante.aprobado = True
                        estudiante.save()
                    elif action == 'delete':
                        user = estudiante.user
                        estudiante.delete()
                        user.delete()
                elif user_type == 'profesor':
                    profesor = Profesor.objects.get(pk=user_id)
                    if action == 'approve':
                        profesor.aprobado = True
                        profesor.save()
                    elif action == 'delete':
                        user = profesor.user
                        profesor.delete()
                        user.delete()
            except Estudiante.DoesNotExist:
                messages.error(request, 'El estudiante seleccionado no existe.')
            except Profesor.DoesNotExist:
                messages.error(request, 'El profesor seleccionado no existe.')

            return redirect('approve')

        return render(request, 'approve_users.html', {
            'estudiantes_pendientes': estudiantes_pendientes,
            'profesores_pendientes': profesores_pendientes
        })


def aprobarEst(request):
    return render(request, "approve_students.html")

def aprobarProf(request):
    return render(request, "approve_teachers.html")