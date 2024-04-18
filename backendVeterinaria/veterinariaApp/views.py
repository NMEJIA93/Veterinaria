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
#logica de asistencia
            #try:
                #tipo = "asistencia"
                #Falta validar que la asistencia solo filtre la del dia actual
                #fechaAsistencia = date.today().strftime('%Y-%m-%d')
                #asistencia = Asistencia.objects.filter(cedula=personalClinica,fechaRegistro=fechaAsistencia)
                #if asistencia.exists():
                #    raise Exception("El usuario ya registro Asistencia")
                #asistencia = Asistencia(tipo=tipo,cedula=personalClinica,fechaRegistro=fechaAsistencia)
                #asistencia.save()
                #message+=" registro de asistencia exitoso"
               # status = 200
            #except Exception as error:
            #    message += str(error)
            #    status = 200
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
            #dd, mm, yyy = fecha_nacimiento.split('/')
            #fecha_nacimiento = f"{yyy}-{mm}-{dd}"
            #pacienteActualizado = Paciente(nombre,cedula,fecha_nacimiento, genero, direccion, email, telefono)
            PropietarioActualizado.nombre=nombre
            #agregar los otros campos del paciente
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
            #parametros Paciente
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
            #dd, mm, yyy = fecha_nacimiento.split('/')
            #fecha_nacimiento = f"{yyy}-{mm}-{dd}"
            propietario_new = PropietarioMascota(nombre=nombre,cedula=cedula, direccion=direccion, email=email, telefono=telefono)
            propietario_new.save()
            #historiaClinica={"_id":propietario_new.cedula,"historias":{}}
            #collection.insert_one(historiaClinica)
            message= "Propietario Grabado con exito\n"
            #try:
            #    nombreContacto = body["nombreContacto"]
            #    relacion = body["relacion"]
           #    telefonocontacto = body["telefonocontacto"]
           #    validadorGeneral.validarNombre(nombreContacto)
           #    controlPacientes.validarParentesco(relacion)
           #    validadorGeneral.validarTelefono(telefonocontacto) 
           #    contacto = informaContacto(paciente = paciente_new,nombre = nombreContacto,relacion = relacion,telefono = telefonocontacto)
           #    contacto.save()    
           #    message+="El contacto se registro correctamente\n"
           #except Exception as error:
            #    print("Error al registrar el contacto paciente:\n"+str(error))
            #    raise Exception("Error al registrar el contacto paciente:\n"+str(error)) 

           #if ("idSeguro" in body and "nombreAseguradora" in body and "vigencia"in body) in body:
           #    try:
           #        idSeguro = body["idSeguro"]
           #        nombreAseguradora = body["nombreAseguradora"]
           #        FechaVigencia = body["vigencia"]
           #        #estado = body["estado"]
           #        validadorGeneral.validarNombre(nombreAseguradora)
           #        controlSeguros.validarPoliza(idSeguro)
           #        validadorGeneral.validar_fecha(FechaVigencia)
           #        #validadorGeneral.validarEstado(estado)
           #        dd, mm, yyy = FechaVigencia.split('/')
           #        FechaVigencia = f"{yyy}-{mm}-{dd}"
           #        
           #        seguro_new = SeguroPaciente.objects.filter(idSeguro=idSeguro)
           #        if seguro_new.exists():
           #            raise Exception("Ya Existe un Seguro con este ID")
           #        seguro_new = SeguroPaciente(idSeguro = idSeguro,nombreAseguradora = nombreAseguradora,paciente = paciente_new,vigencia = FechaVigencia,estado = 1)
           #        seguro_new.save()    
           #        message=+" El Seguro se registro correctamente \n"
           #    except Exception as error:
           #        print("Error al registrar el Seguro paciente:\n"+str(error))
           #        raise Exception("Error al registrar el contacto paciente:\n"+str(error)) 

            status= 200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message}
        return JsonResponse(response,status=status)   
    
    """ def delete(self,request,id):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ADM"])   
            paciente = Paciente.objects.get(cedula=id)
            paciente.estado = 0
            paciente.save()
            message = "usuario Eliminado"
            status=200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message} 
        return JsonResponse(response,status=status) """
    

    