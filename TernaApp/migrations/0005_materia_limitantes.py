# Generated by Django 5.0 on 2024-05-28 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TernaApp', '0004_rename_apellido_profesor_apellidopaterno'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='limitantes',
            field=models.ManyToManyField(blank=True, to='TernaApp.materia'),
        ),
    ]
