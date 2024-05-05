from django.db import models

# Create your models here.

class PersonalClinica(models.Model):
    nombre = models.CharField(max_length=30, null=False)
    cedula = models.BigIntegerField(primary_key=True, null=False, blank=False)
    email = models.CharField(null=False, max_length=30)
    telefono = models.CharField(max_length=10, null=False)
    fecha_nacimiento = models.DateField(null=False)
    direccion = models.CharField(max_length=30)
    rol = models.CharField(max_length=3, null=False, blank=False)
    usuario = models.CharField(null=False, blank=False, max_length=100)
    password = models.CharField(null=False, blank=False, max_length=20)
    estado = models.IntegerField(null=False, blank=False)

# Modelo de la tabla Sesion en la Base de Datos
class Sesion(models.Model):
    id=models.AutoField(primary_key=True)
    usuario=models.ForeignKey(PersonalClinica, on_delete=models.CASCADE, null=True)
    token=models.CharField(max_length=200,null=False,default="")

""" 
class Mascota(models.Model):
    nombre = models.CharField(max_length=30, null=False)
    id = models.BigIntegerField(primary_key=True, null=False, blank=False)
    raza = models.CharField(max_length=30, null=False)
    Especie = models.CharField(max_length=30, null=False)
    fecha_nacimiento = models.DateField(null=False)
    nombrePropietario = models.CharField(max_length=30, null=False)
    cedulaPropietario = models.BigIntegerField(primary_key=True, null=False, blank=False)
    telefonoPropietario = models.CharField(max_length=10, null=False)
    emailPropietario = models.CharField(null=False, max_length=30) """

#Tablas relacionadas a Mascotas

class PropietarioMascota(models.Model):
    nombre = models.CharField(max_length=30, null=False)
    cedula = models.BigIntegerField(primary_key=True, null=False, blank=False)
    telefono = models.CharField(max_length=10, null=False)
    email = models.CharField(null=False, max_length=30)
    direccion = models.CharField(max_length=30, null=True)
    estado = models.IntegerField(null=False, blank=False,default=1)

class Mascota(models.Model):
    nombre = models.CharField(max_length=30, null=False)
    id = models.BigIntegerField(primary_key=True, null=False, blank=False)
    raza = models.CharField(max_length=30, null=False)
    Especie = models.CharField(max_length=30, null=False)
    fecha_nacimiento = models.DateField(null=False)
    propietario = models.ForeignKey(PropietarioMascota, on_delete=models.CASCADE)
    estado = models.IntegerField(null=False, blank=False,default=1)