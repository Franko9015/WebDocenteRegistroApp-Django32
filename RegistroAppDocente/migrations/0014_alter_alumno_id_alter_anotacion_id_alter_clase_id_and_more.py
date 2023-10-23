# Generated by Django 4.2.2 on 2023-10-23 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RegistroAppDocente', '0013_remove_alumno_clase_alumno_curso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='anotacion',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='clase',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='comunicado',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='curso',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='materia',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='notas',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='periodosemestral',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
