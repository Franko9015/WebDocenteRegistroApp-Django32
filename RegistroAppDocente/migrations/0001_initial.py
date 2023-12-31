# Generated by Django 4.2.5 on 2023-10-12 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidoP', models.CharField(max_length=100)),
                ('apellidoM', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('foto_alumno', models.ImageField(blank=True, null=True, upload_to='foto')),
                ('asistencias', models.PositiveIntegerField(default=0)),
                ('clases_programadas', models.PositiveIntegerField(default=0)),
                ('Reprobado', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'alumno',
            },
        ),
        migrations.CreateModel(
            name='Comunicado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('contenido', models.TextField()),
                ('fecha_envio', models.DateTimeField(auto_now_add=True)),
                ('es_urgente', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombrecurso', models.CharField(max_length=100)),
                ('aniocurso', models.IntegerField(blank=True, null=True)),
                ('cantidadalumnos', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Curso',
            },
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'materia',
            },
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidoP', models.CharField(max_length=100)),
                ('apellidoM', models.CharField(max_length=100)),
                ('foto_perfil', models.ImageField(blank=True, null=True, upload_to='foto')),
                ('titulo', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('cantidad_alumnos', models.IntegerField()),
                ('correo', models.EmailField(max_length=100, unique=True)),
                ('telefono', models.CharField(blank=True, max_length=15, null=True)),
                ('redes_sociales', models.CharField(blank=True, max_length=100, null=True)),
                ('cursos', models.ManyToManyField(to='RegistroAppDocente.curso')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RegistroAppDocente.materia')),
            ],
            options={
                'db_table': 'profesor',
            },
        ),
        migrations.CreateModel(
            name='Notas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parcial1', models.DecimalField(decimal_places=1, max_digits=3)),
                ('parcial2', models.DecimalField(decimal_places=1, max_digits=3)),
                ('parcial3', models.DecimalField(decimal_places=1, max_digits=3)),
                ('parcial4', models.DecimalField(decimal_places=1, max_digits=3)),
                ('examen_final', models.DecimalField(decimal_places=1, max_digits=3)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RegistroAppDocente.alumno')),
            ],
            options={
                'db_table': 'notas',
            },
        ),
        migrations.AddField(
            model_name='alumno',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RegistroAppDocente.curso'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RegistroAppDocente.materia'),
        ),
    ]
