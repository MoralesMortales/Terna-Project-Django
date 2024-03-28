from .views import BasePage, FormularioEmail, contactar
from django.urls import path

urlpatterns = [
   path("", FormularioEmail.as_view(), name="Base"),
   path("contactar/", contactar, name="contactar")
]
