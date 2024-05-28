
from django.contrib.auth.models import User
from django import forms
from .models import Materia, Carrera, Estudiante, Secretario, NotaEstudiante, Profesor


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
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_conf = cleaned_data.get('password_conf')

        if password and password_conf and password != password_conf:
            self.add_error('password_conf', 'Las contraseñas no coinciden.')

        return cleaned_data
class ProfesorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_conf = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profesor
        fields = [
            'nombre', 'apellidoPaterno', 'cedula',
            'fechaNacimiento', 'sexo', 'email', 'telefono'
        ]
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_conf = cleaned_data.get('password_conf')

        if password and password_conf and password != password_conf:
            self.add_error('password_conf', 'Las contraseñas no coinciden.')

        return cleaned_data


class NotaEstudianteForm(forms.ModelForm):
    class Meta:
        model = NotaEstudiante
        fields = ['estudiante', 'primer_corte',
                  'segundo_corte', 'tercer_corte']


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
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_conf = cleaned_data.get('password_conf')

        if password and password_conf and password != password_conf:
            self.add_error('password_conf', 'Las contraseñas no coinciden.')

        return cleaned_data


class MateriasForm:
    class Meta:
        model = Materia
        fields = [
            'codigo', 'nombre',
            'creditos', 'profesor', 'limite_estudiantes'
        ]


class AprobarEstudianteForm:
    class Meta:
        model = Estudiante
        fields = [
            'aprobado'
        ]

class AprobarProfesorForm:

    class Meta:
        model = Estudiante
        fields = [
            'aprobado'
        ]
