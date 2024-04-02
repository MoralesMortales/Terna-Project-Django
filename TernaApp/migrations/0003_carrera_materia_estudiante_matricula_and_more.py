# Generated by Django 5.0 on 2024-04-02 01:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TernaApp', '0002_remove_estudiante_carrera_remove_matricula_curso_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('codigo', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('duracion', models.PositiveSmallIntegerField(default=5)),
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
            name='Estudiante',
            fields=[
                ('cedula', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=60)),
                ('apellidoPaterno', models.CharField(max_length=30)),
                ('apellidoMaterno', models.CharField(max_length=30)),
                ('fechaNacimiento', models.DateTimeField()),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='F', max_length=1)),
                ('vigencia', models.BooleanField(default=True)),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TernaApp.carrera')),
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
        migrations.DeleteModel(
            name='StudentExtra',
        ),
    ]
