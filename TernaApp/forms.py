
from django.contrib.auth.models import User
from django import forms
from .models import Carrera, Estudiante, Secretario, NotaEstudiante

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

class NotaEstudianteForm(forms.ModelForm):
    class Meta:
        model = NotaEstudiante
        fields = ['estudiante', 'primer_corte', 'segundo_corte', 'tercer_corte']

class EditarNotaEstudianteForm(forms.ModelForm):
    class Meta:
        model = NotaEstudiante
        fields = ['primer_corte', 'segundo_corte', 'tercer_corte']

class SecretarioForm(forms.ModelForm):  
    password = forms.CharField(widget=forms.PasswordInput)
    password_conf = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Secretario
        fields = [
            'nombre', 'apellidoPaterno', 'cedula', 
            'fechaNacimiento', 'sexo', 'email', 'telefono'
        ]