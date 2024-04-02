# Generated by Django 5.0 on 2024-04-02 03:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TernaApp', '0004_alter_estudiante_fechanacimiento'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='apellidoMaterno',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='apellidoPaterno',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='cedula',
            field=models.CharField(default='', max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='fechaNacimiento',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='nombres',
            field=models.CharField(default='', max_length=60),
        ),
    ]
