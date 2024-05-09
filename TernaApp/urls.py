from .views import BasePage,logIn,logOut,signUp,menuDefaultPage, createNew, ugmaPage
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
] 
