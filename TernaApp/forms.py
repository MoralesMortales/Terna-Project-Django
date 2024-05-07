
from django.contrib.auth.models import User
from django import forms
from .models import Carrera, Estudiante, Imagen, publicaciones

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
        
        def clean_username(self):
            username = self.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Este nombre de usuario ya está en uso. Por favor, elija otro.")
            return username
            
class ImagenForm(forms.ModelForm):
    class Meta:
        model = publicaciones
        fields = ['nombre', 'description', 'imagen']