from datetime import datetime,date
from typing import Any
from django import http
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import PersonalClinica,Sesion
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
