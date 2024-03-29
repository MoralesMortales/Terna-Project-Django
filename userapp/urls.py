
from django.urls import path
from .views import homePage,productsPage,exit

urlpatterns = [
    path('', homePage, name = "home"),
    path('products/', productsPage, name = "products"),
    path('logout/', exit, name = "exit"),

]
