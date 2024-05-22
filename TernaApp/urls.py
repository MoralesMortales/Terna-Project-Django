from .views import menuDefaultPage, logIn, logOut, signUp, createNew, ugmaPage, signup_S, editar_notas_estudiante, listar_notas, lista_estudiantes #type:ignore
from django.urls import path #type:ignore
from django.conf.urls.static import static #type:ignore
from django.conf import settings #type:ignore

urlpatterns = [
   path("", menuDefaultPage, name="menuDefault"),
   path("login", logIn, name="Login"),
   path("logout", logOut, name="Logout"),
   path("signup", signUp, name="Signup"),
   path("createNew", createNew, name="Create"),
   path("Ugma", ugmaPage, name="UgmaPage"),
   path("signup_S", signup_S, name="signup_s"),
   path("notas/editar/<str:email>/", editar_notas_estudiante, name="editarNotas"),
   path("listar_notas", listar_notas, name="listar_notas"),
   path("lista_estudiantes", lista_estudiantes, name="lista_est"),

] 
