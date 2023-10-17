# Generated by Django 4.2.5 on 2023-10-15 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RegistroAppDocente', '0009_periodosemestral_remove_alumno_clases_programadas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clase',
            name='materia',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='RegistroAppDocente.materia'),
        ),
        migrations.AddField(
            model_name='curso',
            name='asignaturas',
            field=models.ManyToManyField(through='RegistroAppDocente.Clase', to='RegistroAppDocente.materia'),
        ),
    ]