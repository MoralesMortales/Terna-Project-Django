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


class publicaciones(models.Model):
    nombre = models.CharField(max_length=100)
    description = models.TextField(max_length=1200)
    imagen = models.ImageField(upload_to='imagenes/')


class Imagen(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes/')

    def save(self, *args, **kwargs):
        # Si la instancia de Imagen aún no tiene un ID asignado, es una nueva instancia
        if not self.pk:
            # Guarda la instancia para obtener un ID asignado
            super().save(*args, **kwargs)
            # Asigna el ID recién asignado a publicaciones_id
            self.publicaciones_id = self.pk
        # Guarda la instancia nuevamente con el publicaciones_id asignado
        super().save(*args, **kwargs)


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

    def nombreCompleto(self):
        txt = "{0} {1} {2}"
        return txt.format(self.nombre, self.apellidoPaterno, self.apellidoMaterno)

    def __str__(self):

        txt = "Secretari@: {0}"
        return txt.format(self.nombreCompleto())


class Materia(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    seccion = models.CharField(max_length=10)
    nombre = models.CharField(max_length=30)
    creditos = models.SmallIntegerField(default=5)
    profesor = models.CharField(max_length=70)


class Matricula(models.Model):
    id = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(
        Estudiante, null=False, blank=False, on_delete=models.CASCADE)
    materia = models.ForeignKey(
        Materia, null=False, blank=False, on_delete=models.CASCADE)
    fechaMatricula = models.DateTimeField(auto_now_add=True)
