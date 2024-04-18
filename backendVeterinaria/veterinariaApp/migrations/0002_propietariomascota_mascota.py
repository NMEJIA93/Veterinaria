# Generated by Django 4.1.13 on 2024-04-18 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('veterinariaApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropietarioMascota',
            fields=[
                ('nombre', models.CharField(max_length=30)),
                ('cedula', models.BigIntegerField(primary_key=True, serialize=False)),
                ('telefono', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('nombre', models.CharField(max_length=30)),
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('raza', models.CharField(max_length=30)),
                ('Especie', models.CharField(max_length=30)),
                ('fecha_nacimiento', models.DateField()),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='veterinariaApp.propietariomascota')),
            ],
        ),
    ]
