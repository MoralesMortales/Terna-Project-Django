from django.db import models
from django.contrib.auth.models import User
from requests import request


class Carrera(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=60)
    duracion = models.PositiveSmallIntegerField(default=5)

    def __str__(self):
        txt = "{0}"
        return txt.format(self.nombre)

class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    cedula = models.CharField(max_length=8, unique=True)
    telefono = models.CharField(max_length=13, blank=True)
    nombre = models.CharField(max_length=30)
    email = models.CharField(max_length=50, blank=True, primary_key=True)
    apellidoPaterno = models.CharField(max_length=30, blank=True)
    apellidoMaterno = models.CharField(max_length=30, blank=True)
    fechaNacimiento = models.DateField(default='2000-01-01')
    sexos = [

        ('M', 'Masculino'),
        ('F', 'Femenino')

    ]
    sexo = models.CharField(max_length=1, choices=sexos, default='F')
    carrera = models.ForeignKey(
        Carrera, null=False, blank=True, on_delete=models.CASCADE)
    vigencia = models.BooleanField(default=True)

    def nombreCompleto(self):
        txt = "{0} {1} {2}"
        return txt.format(self.nombre, self.apellidoPaterno, self.apellidoMaterno)

    def __str__(self):

        if self.vigencia:
            vigente_act = "VIGENTE"

        else:
            vigente_act = "NO VIGENTE"

        txt = "{0} | {1}"
        return txt.format(self.nombreCompleto(), vigente_act)

class Secretario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    cedula = models.CharField(max_length=9, unique=True)
    telefono = models.CharField(max_length=13, blank=True)
    apellidoPaterno = models.CharField(max_length=30, blank=True)
    nombre = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=50, blank=True, primary_key=True)
    fechaNacimiento = models.DateField(default='2000-01-01')
    sexos = [

        ('M', 'Masculino'),
        ('F', 'Femenino')

    ]
    sexo = models.CharField(max_length=1, choices=sexos, default='F')

    def nombreCompleto(self):
        txt = "{0}"
        return txt.format(self.nombre)

    def __str__(self):
        txt = "Secretari@: {0}"
        return txt.format(self.nombreCompleto())

class NotaEstudiante(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    primer_corte = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    segundo_corte = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    tercer_corte = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    nota_definitiva = models.DecimalField(max_digits=4, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.nota_definitiva = self.calcular_nota_definitiva()
        super().save(*args, **kwargs)

    def calcular_nota_definitiva(self):
        return (self.primer_corte + self.segundo_corte + self.tercer_corte) / 3

    def __str__(self):
        return f"Notas de {self.estudiante} - Definitiva: {self.nota_definitiva}"


class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Materia(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    seccion = models.CharField(max_length=10)
    nombre = models.CharField(max_length=30)
    creditos = models.SmallIntegerField(default=5)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.nombre} - {self.seccion}'


