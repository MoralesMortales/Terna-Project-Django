from .views import BasePage,logIn,logOut,signUp,menuDefaultPage
from django.urls import path

urlpatterns = [
   path("", menuDefaultPage, name="menuDefault"),
   path("login", logIn, name="Login"),
   path("logout", logOut, name="Logout"),
   path("signup", signUp, name="Signup"),
]
