# Generated by Django 4.2.5 on 2023-10-12 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RegistroAppDocente', '0002_alumno_username_profesor_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='foto_alumno',
            field=models.ImageField(blank=True, default='foto/fotodefault.png', null=True, upload_to='foto'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='foto_perfil',
            field=models.ImageField(blank=True, default='foto/fotodefault.png', null=True, upload_to='foto'),
        ),
    ]