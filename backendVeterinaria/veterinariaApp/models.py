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

# Models relacionados a consulta

class Medicamento(models.Model):
    idMedicamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    presentacion = models.CharField(max_length=30, null=False)
    precio =  models.FloatField(null=False, blank=False)

class Procedimiento(models.Model):
    codProcedimiento = models.AutoField(primary_key=True)
    nombreProcedimiento = models.CharField(max_length=30, null=False)
    precio = models.FloatField(null=False, blank=False)

class Ayuda(models.Model):
    codAyuda = models.AutoField(primary_key=True)
    nombreAyuda = models.CharField(max_length=30, null=False)
    precio = models.FloatField(null=False, blank=False)

class Orden(models.Model):
    id = models.AutoField(primary_key=True)
    idMascota = models.ForeignKey(Mascota, null=False, on_delete=models.CASCADE)
    cedulaMedico = models.ForeignKey(PersonalClinica, null=False, on_delete=models.CASCADE)
    fechaRegistro = models.DateField(null=False)
    estado = models.IntegerField(null=False, blank=False, default = 1)

class OrdenMedicamento(models.Model):
    id = models.AutoField(primary_key=True)
    idOrden = models.ForeignKey(Orden, null=False, on_delete=models.CASCADE)
    item = models.IntegerField(null=False, blank=False, default = 0)
    idMedicamento = models.ForeignKey(Medicamento, null=False, on_delete=models.CASCADE)
    dosis = models.CharField(max_length=30, null=False)
    tiempoTratamiento = models.IntegerField(null=False, blank=False, default = 0)

class OrdenProcedimiento(models.Model):
    id = models.AutoField(primary_key=True)
    idOrden = models.ForeignKey(Orden, null=False, on_delete=models.CASCADE)
    item = models.IntegerField(null=False, blank=False, default = 0)
    cantidad = models.IntegerField(null=True)
    idProcedimiento = models.ForeignKey(Procedimiento, null=False, on_delete=models.CASCADE)
    asistenciaEspecializada = models.CharField(max_length=30, null=False)

class OrdenAyudaDiagnostica(models.Model):
    id = models.AutoField(primary_key=True)
    idOrden = models.ForeignKey(Orden, null=False, on_delete=models.CASCADE)
    item = models.IntegerField(null=False, blank=False, default = 0)
    cantidad = models.IntegerField(null=True)
    idAyuda = models.ForeignKey(Ayuda, null=True, on_delete=models.CASCADE)
    asistenciaEspecializada = models.CharField(max_length=30, null=False)
    revision = models.BooleanField(null=False,default=False)
