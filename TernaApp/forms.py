
from django.contrib.auth.models import User
from django import forms
from .models import Carrera, Estudiante

class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ['codigo', 'nombre', 'duracion']
        
class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'
        widgets = {
            'sexo': forms.Select(choices=Estudiante.sexos),
        }