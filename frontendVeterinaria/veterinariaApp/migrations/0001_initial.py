# Generated by Django 4.1.13 on 2024-04-10 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sesion',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('token', models.CharField(default='', max_length=200)),
            ],
        ),
    ]
