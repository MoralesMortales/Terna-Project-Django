
from django.contrib.auth.models import User
from django import forms
from .models import Carrera

class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ['codigo', 'nombre', 'duracion']