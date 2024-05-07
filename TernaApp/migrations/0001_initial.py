# Generated by Django 5.0 on 2024-05-07 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('codigo', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=60)),
                ('duracion', models.PositiveSmallIntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('imagen', models.ImageField(upload_to='imagenes/')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('codigo', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('seccion', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=30)),
                ('creditos', models.SmallIntegerField(default=5)),
                ('profesor', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='publicaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1200)),
                ('imagen', models.ImageField(upload_to='imagenes/')),
            ],
        ),
        migrations.CreateModel(
            name='Secretario',
            fields=[
                ('cedula', models.CharField(max_length=8, unique=True)),
                ('telefono', models.CharField(blank=True, max_length=13)),
                ('nombre', models.CharField(max_length=30)),
                ('email', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False)),
                ('apellidoPaterno', models.CharField(blank=True, max_length=30)),
                ('apellidoMaterno', models.CharField(blank=True, max_length=30)),
                ('fechaNacimiento', models.DateField(default='2000-01-01')),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='F', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('cedula', models.CharField(max_length=8, unique=True)),
                ('telefono', models.CharField(blank=True, max_length=13)),
                ('nombre', models.CharField(max_length=30)),
                ('email', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False)),
                ('apellidoPaterno', models.CharField(blank=True, max_length=30)),
                ('apellidoMaterno', models.CharField(blank=True, max_length=30)),
                ('fechaNacimiento', models.DateField(default='2000-01-01')),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='F', max_length=1)),
                ('vigencia', models.BooleanField(default=True)),
                ('carrera', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='TernaApp.carrera')),
            ],
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fechaMatricula', models.DateTimeField(auto_now_add=True)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TernaApp.estudiante')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TernaApp.materia')),
            ],
        ),
    ]
