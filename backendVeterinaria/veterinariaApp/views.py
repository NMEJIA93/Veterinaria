from datetime import datetime,date
from typing import Any
from django import http
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import PersonalClinica,Sesion,PropietarioMascota,Mascota
from backendVeterinaria.conexionMongo import collection
import json,secrets,string
from .helpers import validadorGeneral, validadorPersonalClinica, controlPacientes, validadorNovedades,validadorEnfermeras, controlSeguros, controlFacturas, validadorOrdenes
from .helpers import controlOrdenes, controlPersonalClinica, validadorMedicos
from django.db.models import Max

# Create your views here.

def validarRol(sesion,rol):
    print(sesion.usuario.nombre)
    if sesion.usuario.rol not in rol and sesion.usuario.usuario!="superAdmin":
        raise Exception("el usuario no posee permisos")
    
class Logueo(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        #login = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            #validarRol(sesion,["ADM"])
            rol=sesion.usuario.rol
            status=200
            message = "paso la validacion"
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "rol": rol}
        return JsonResponse(response,status=status) 

    def put(self,request):
        pass

    def post(self, request):
        token=""
        message=""
        try:
            body = json.loads(request.body)
            rol = body["rol"]
            usuario=body["usuario"]
            password=body["contraseña"]
            personalClinica = PersonalClinica.objects.get(usuario=usuario,rol=rol,password=password,estado=1)
            sesion = Sesion.objects.filter(usuario=personalClinica)
            if sesion.exists():
                raise Exception("El usuario ya esta en sesion")
            caracteres = string.ascii_letters + string.digits
            token = ''.join(secrets.choice(caracteres) for _ in range(128))
            sesion = Sesion(usuario=personalClinica,token=token)
            
            sesion.save()
            message += "Login Exitoso"
            status = 200
        except Exception as error:
            message += str(error)
            status = 400
        response = {"message": message, "token":token}
        print('el error esta antes del return')
        print(response)
        print(status)
        return JsonResponse(response,status=status)

    def delete(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion=Sesion.objects.get(token=token)
            sesion.delete()
            message="se ha cerrado sesion"
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message}
        return JsonResponse(response,status=status)  


class Propietario(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    def get(self,request,id=None):
        Propietarios = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ADM"])
            if id:
                Propietarios = list(PropietarioMascota.objects.filter(cedula=id,estado=1).values())
            else:
                Propietarios = list(PropietarioMascota.objects.values())
                
            if len(Propietarios)>0:
                message = "No hay propietarios registrados"
            else:
                message="Propietarios no encontrados"
                status = 400
                raise Exception("Propietarios no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Propietarios": Propietarios}
        return JsonResponse(response,status=status)

    def put(self,request):
        PropietarioActualizado=""
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["ADM"])
            body=json.loads(request.body)
            cedula=body["cedula"]            
            #actualizar datos
            PropietarioActualizado = PropietarioMascota.objects.get(cedula=cedula)
            nombre = body["nombre"]           
            telefono = body["telefono"]
            direccion = body["direccion"]           
            email = body["email"]
            validadorGeneral.validarNombre(nombre)
            validadorGeneral.validarEmail(email)
            validadorGeneral.validarTelefono(telefono)
            validadorGeneral.validarDireccion(direccion)
            PropietarioActualizado.nombre=nombre
            #agregar los otros campos del Propietario
            PropietarioActualizado.telefono=telefono
            PropietarioActualizado.direccion=direccion
            PropietarioActualizado.email=email
            PropietarioActualizado.save()                                       
            message= "Propietario Actualizado con exito"
            status= 200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message}
        return JsonResponse(response,status=status)

    def post(self,request):
        propietario_new=""
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["ADM"])
            body=json.loads(request.body)
            #parametros Propietario
            cedula=body["cedula"]
            nombre = body["nombre"]
            telefono = body["telefono"]    
            direccion = body["direccion"]         
            email = body["email"]
            validadorGeneral.validarNombre(nombre)
            validadorGeneral.validarCedula(cedula)
            validadorGeneral.validarEmail(email)
            validadorGeneral.validarTelefono(telefono)
            validadorGeneral.validarDireccion(direccion)
            propietario_new=PropietarioMascota.objects.filter(cedula=cedula)
            #valida que no exista
            print(propietario_new)
            if propietario_new.exists():
                raise Exception ("El Propietario ya existe")   
            propietario_new = PropietarioMascota(nombre=nombre,cedula=cedula, direccion=direccion, email=email, telefono=telefono)
            propietario_new.save()
            message= "Propietario Grabado con exito\n"
            status= 200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message}
        return JsonResponse(response,status=status)   
    
    def delete(self,request,id):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ADM"])   
            propietario = PropietarioMascota.objects.get(cedula=id)
            propietario.estado = 0
            propietario.save()
            message = "usuario Eliminado"
            status=200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message} 
        return JsonResponse(response,status=status) 
    

class ModuloMascota(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    def get(self,request,id=None):
        Mascotas = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ADM"])
            if id:
                Mascotas = list(Mascota.objects.filter(id=id,estado=1).values())
            else:
                Mascotas = list(Mascota.objects.values())
                
            if len(Mascotas)>0:
                message = "No hay Mascotas registradas"
            else:
                message="No hay mascotas registradas"
                status = 400
                raise Exception("No hay mascotas registradas")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Mascotas": Mascotas}
        return JsonResponse(response,status=status)

    def put(self,request):
        mascotaActualizada=""
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["ADM"])
            body=json.loads(request.body)
            idMascota=body["idMascota"]            
            #actualizar datos
            mascotaActualizada = Mascota.objects.get(id=idMascota)
            #parametros Mascota
            nombre = body["nombreMascota"]
            raza = body["raza"]
            especie = body["especie"]
            fecha_nacimiento = body["fechanace"] 
            dd, mm, yyy = fecha_nacimiento.split('/')
            fecha_nacimiento = f"{yyy}-{mm}-{dd}"
            mascotaActualizada.nombre=nombre
            mascotaActualizada.nombre=raza
            mascotaActualizada.nombre=especie
            mascotaActualizada.nombre=fecha_nacimiento
            mascotaActualizada.save()                                       
            message= "Mascota Actualizada con Exito"
            status= 200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message}
        return JsonResponse(response,status=status)

    def post(self,request):
        mascota_new=""
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["ADM"])
            body=json.loads(request.body)
            #parametros Paciente
            nombre = body["nombreMascota"]
            id=body["id"]
            raza = body["raza"]
            especie = body["especie"]
            fecha_nacimiento = body["fechanace"] 
            validadorGeneral.validarNombre(nombre)
            #faltan validaciones 

            mascota_new=PropietarioMascota.objects.filter(id=id)
            #valida que no exista
            print(mascota_new)
            if mascota_new.exists():
                raise Exception ("La Mascota Ya Existe")           
            dd, mm, yyy = fecha_nacimiento.split('/')
            fecha_nacimiento = f"{yyy}-{mm}-{dd}"
            if ("nombrePeopietario" in body and "cedula" in body and "telefono"in body and "email"in body and "direccion"in body) in body:
                try:
                    #parametros Propietario
                    cedula=body["cedulaPropietario"]
                    nombre = body["nombrePropietario"]
                    telefono = body["telefono"]    
                    direccion = body["direccion"]         
                    email = body["email"]
                    validadorGeneral.validarNombre(nombre)
                    validadorGeneral.validarCedula(cedula)
                    validadorGeneral.validarEmail(email)
                    validadorGeneral.validarTelefono(telefono)
                    validadorGeneral.validarDireccion(direccion)
                    propietario_new=PropietarioMascota.objects.filter(cedula=cedula)
                    #valida que no exista
                    print(propietario_new)
                    if propietario_new.exists():
                        raise Exception ("El Propietario ya existe")
                    propietario_new = PropietarioMascota(nombre=nombre,cedula=cedula, direccion=direccion, email=email, telefono=telefono)
                    propietario_new.save()
                    message= "Propietario Grabado con exito\n"
                except Exception as error:
                    print("Error al registrar el contacto paciente:\n"+str(error))
                    raise Exception("Error al registrar el contacto paciente:\n"+str(error)) 
                
            if ("cedulaPropietario" in body ) in body:
                cedula = body["cedulaPropietario"]
                validadorGeneral.validarCedula(cedula)
            #
            mascota_new = Mascota(nombre=nombre,id=id,raza=raza, Especie=especie, fecha_nacimiento=fecha_nacimiento, propietario=cedula)
            mascota_new.save()
            historiaClinica={"_id":mascota_new.id,"historias":{}}
            carnetVacunas={"_id":mascota_new.id,"historias":{}}
            collection.insert_one(historiaClinica)
            collection.insert_one(carnetVacunas)
            message= "Mascota Grabado con exito\n"
            status= 200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message}
        return JsonResponse(response,status=status)   
    
    def delete(self,request,id):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ADM"])   
            mascota = Mascota.objects.get(id=id)
            mascota.estado = 0
            mascota.save()
            message = "usuario Eliminado"
            status=200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message} 
        return JsonResponse(response,status=status) 
    

class ModuloPersonalClinica(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any,**kwargs:Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id=None):
        personalClinica = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["RH"])
            if id:
                personalClinica = list(PersonalClinica.objects.filter(cedula=id,estado=1).values())
            else:
                personalClinica = list(PersonalClinica.objects.values())
            print(personalClinica)    
            if len(personalClinica)>0:
                message = "registros encontrados"
            else:
                message="registros Personal clinica no encontrados"
                status = 400
                raise Exception("Registros Personal clinica no encontrados")
            status=200
        except Exception as error:
            message='Error al buscar personal clinica - persona no encontrada'
            status = 400
            raise Exception('Registros no encontrados')
        response = {"message":  message, "Empleados": personalClinica}
        return JsonResponse(response,status)
    
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["RH"])
            body = json.loads(request.body)
            nombre = body["nombre"]
            cedula = body["cedula"]
            email = body["email"]
            telefono = body["telefono"]
            fecha_nacimiento = body["fechanace"]
            direccion = body["direccion"]
            rol = body["rol"]
            usuario = body["usuario"]
            password = body["password"]
            
            validadorGeneral.validarNombre(nombre)
            validadorGeneral.validarCedula(cedula)
            validadorGeneral.validarEmail(email)
            validadorGeneral.validarTelefono(telefono)
            validadorGeneral.validar_fecha(fecha_nacimiento)
            validadorPersonalClinica.validarDatosUsuario(rol,usuario,password)
            validadorGeneral.ValidarPassword(password)
            empleado_new = PersonalClinica.objects.filter(cedula=cedula)
            if empleado_new.exists():
                raise Exception("Ya Existe un empleado registrado con esa Cedula")
            empleado_new = PersonalClinica.objects.filter(usuario=usuario)
            if empleado_new.exists():
                raise Exception("Ya Existe un empleado registrado con ese Usuario")
            dd, mm, yyy = fecha_nacimiento.split('/')
            fecha_nacimiento = f"{yyy}-{mm}-{dd}"
            empleado_new = PersonalClinica(nombre=nombre,cedula=cedula,email=email,telefono=telefono,fecha_nacimiento=fecha_nacimiento,direccion=direccion,rol=rol,usuario=usuario,password=password,estado=1)
            empleado_new.save()
            message = "usuario Registrado"
            status=200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)
    
    def put(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["RH"])
            body = json.loads(request.body)
            nombre = body["nombre"]
            cedula = body["cedula"]
            email = body["email"]
            telefono = body["telefono"]
            fecha_nacimiento = body["fechanace"]
            direccion = body["direccion"]
            rol = body["rol"]
            usuario = body["usuario"]
            password = body["password"]
            validadorGeneral.validarNombre(nombre)
            #validadorGeneral.validarCedula(cedula)
            validadorGeneral.validarEmail(email)
            validadorGeneral.validarTelefono(telefono)
            validadorGeneral.validar_fecha(fecha_nacimiento)
            validadorPersonalClinica.validarDatosUsuario(rol,usuario,password)
            validadorGeneral.ValidarPassword(password)
            dd, mm, yyy = fecha_nacimiento.split('/')
            fecha_nacimiento = f"{yyy}-{mm}-{dd}"
            empleado_Actualizado = PersonalClinica.objects.get(cedula=cedula)
            empleado_Actualizado.nombre = nombre
            empleado_Actualizado.email = email
            empleado_Actualizado.fecha_nacimiento = fecha_nacimiento
            empleado_Actualizado.direccion = direccion
            empleado_Actualizado.rol = rol
            empleado_Actualizado.usuario = usuario
            empleado_Actualizado.password = password
            empleado_Actualizado.save()
            message = "usuario Actualizado"
            status=200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)
            
    def delete(self,request,id):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["RH"])   
            empleado_Eliminado = PersonalClinica.objects.get(cedula=id)
            empleado_Eliminado.estado = 0
            empleado_Eliminado.save()
            message = "usuario Eliminado"
            status=200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message} 
        return JsonResponse(response,status=status)
    

    

    