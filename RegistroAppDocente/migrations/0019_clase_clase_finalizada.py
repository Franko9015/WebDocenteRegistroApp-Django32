# Generated by Django 4.2.5 on 2023-10-26 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RegistroAppDocente', '0018_merge_20231023_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='clase',
            name='clase_finalizada',
            field=models.BooleanField(default=False),
        ),
    ]
