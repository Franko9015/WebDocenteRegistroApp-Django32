# Generated by Django 4.2.5 on 2023-10-12 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RegistroAppDocente', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profesor',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
    ]