# Generated by Django 5.0 on 2024-05-28 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TernaApp', '0003_remove_materia_seccion_estudiante_aprobado_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profesor',
            old_name='apellido',
            new_name='apellidoPaterno',
        ),
    ]
