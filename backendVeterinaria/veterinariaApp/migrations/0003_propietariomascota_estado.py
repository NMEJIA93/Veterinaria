# Generated by Django 4.1.13 on 2024-04-18 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veterinariaApp', '0002_propietariomascota_mascota'),
    ]

    operations = [
        migrations.AddField(
            model_name='propietariomascota',
            name='estado',
            field=models.IntegerField(default=1),
        ),
    ]