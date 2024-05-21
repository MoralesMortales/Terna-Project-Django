
from django.contrib.auth.models import User
from django import forms
from .models import Carrera, Estudiante, Secretario

class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ['codigo', 'nombre', 'duracion']

class EstudianteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_conf = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Estudiante
        fields = [
            'nombre', 'apellidoPaterno', 'apellidoMaterno', 'cedula', 
            'fechaNacimiento', 'sexo', 'email', 'telefono', 'carrera'
        ]

class SecretarioForm(forms.ModelForm):
    class Meta:
        model = Secretario
        fields = '__all__'
        widgets = {
                'sexo': forms.Select(choices=Estudiante.sexos),
                }
