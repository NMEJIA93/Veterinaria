from datetime import datetime,date
from typing import Any
from django import http
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import PersonalClinica,Sesion,PropietarioMascota,Mascota
from .models import Medicamento,Orden,OrdenMedicamento,Procedimiento,OrdenProcedimiento
from .models import Ayuda,OrdenAyudaDiagnostica
from backendVeterinaria.conexionMongo import collection
from backendVeterinaria.conexionMongo import collection1
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
            validarRol(sesion,["ADM","MED"])
            if id:
                Mascotas = list(Mascota.objects.filter(id=id,estado=1).values())
            else:
                Mascotas = list(Mascota.objects.values())
                
            if len(Mascotas)>0:
                message = "Mascotas registradas"
            else:
                message="No hay mascotas registradas"
                status = 400
                raise Exception("No hay mascotas registradas")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Mascotas": Mascotas}
        print(message)
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
            idMascota=body["idMascota"]
            raza = body["raza"]
            especie = body["especie"]
            fecha_nacimiento = body["fechanace"] 
            validadorGeneral.validarNombre(nombre)
            mascota_new=Mascota.objects.filter(id=idMascota)
            print(mascota_new,"____________")
            print("hola",body)
            if mascota_new.exists():
                raise Exception ("La Mascota Ya Existe")           
            dd, mm, yyy = fecha_nacimiento.split('/')
            fecha_nacimiento = f"{yyy}-{mm}-{dd}"
            if "nombrePropietario" in body and "cedulaPropietario" in body and "telefono"in body and "email"in body and "direccion"in body:
                try:
                    #parametros Propietario
                    print('entro aca')
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
                
            #if ("cedulaPropietario" in body ) in body:
            #    cedula = body["cedulaPropietario"]
            #    validadorGeneral.validarCedula(cedula)
            #
            mascota_new = Mascota(nombre=nombre,id=idMascota,raza=raza, Especie=especie, fecha_nacimiento=fecha_nacimiento, propietario=propietario_new)
            mascota_new.save()
            historiaClinica={"_idHistoria":mascota_new.id,"historias":{}}
            carnetVacunas={"_idCarnet":mascota_new.id,"historias":{}}
            collection.insert_one(historiaClinica)
            collection1.insert_one(carnetVacunas)
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
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=None):
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
            message = str(error)
            status = 400
        response = {"message":message, "Empleados": personalClinica}
        return JsonResponse(response,status=status)
    
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
    
class ModuloMedicamento(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=None):
        medicamentos = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ADM","ENF"])

            if id:
                medicamentos = list(Medicamento.objects.filter(idMedicamento=id).values())
            else:
                medicamentos = list(Medicamento.objects.values())
                
            if len(medicamentos)>0:
                message = "registros encontrados"
            else:
                message="registros no encontrados"
                status = 400
                raise Exception("Registros no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Medicamentos": medicamentos}
        return JsonResponse(response,status=status)
    
    def put(self,request,id=None):
        medicamentoActualizado=""
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["MED","ADM","ENF"])
            body = json.loads(request.body)
            nombre = body["nombre"]
            presentacion = body["presentacion"]
            precio = body["precio"]
            validadorGeneral.validarNombre(nombre)
            validadorMedicos.PresentacionMedicamento(presentacion)
            validadorMedicos.precioMedicamento(precio)
            medicamento_actualizado = Medicamento.objects.filter(idMedicamento=id)
            if not medicamento_actualizado.exists():
                raise Exception("No existe un medicamento con ese ID")
            medicamentoActualizado = Medicamento.objects.get(idMedicamento=id)
            medicamentoActualizado.nombre = nombre
            medicamentoActualizado.presentacion = presentacion
            medicamentoActualizado.precio = precio
            medicamentoActualizado.save()                                       
            message= "Medicamento Actualizado con exito"
            status= 200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message}
        return JsonResponse(response,status=status)
        
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ADM","ENF"])
            body = json.loads(request.body)
            nombre = body["nombre"]
            presentacion = body["presentacion"]
            precio = body["precio"]
            validadorGeneral.validarNombre(nombre)
            medicamento = Medicamento(nombre = nombre,presentacion  = presentacion,precio = precio)
            medicamento.save()    
            message=" El Medicamento se registro correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

    def delete(self,request):
        pass

class ModuloOrdenMedicamento(View):
    #def get(self,request,id=None, cc=None):
    def get(self,request,id=None):
        ordenMedicamento = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ENF"])
            #if id:
            #    print ("ingreso al id")
                #ordenMedicamento = OrdenMedicamento.objects.get(id=id)
            #    ordenMedicamento = list(OrdenMedicamento.objects.filter(id=id).values())
            if id:
                mascota = Mascota.objects.get(id=id)   
                print(mascota)            
                ordenePaciente = Orden.objects.get(cedulaPaciente=mascota.id,estado=1)
                print(ordenePaciente)
                ordenMedicamento = list(OrdenMedicamento.objects.filter(idOrden=ordenePaciente).values())
                print(ordenMedicamento)
                for oMedicamento in ordenMedicamento:
                    medicamento=Medicamento.objects.get(idMedicamento=oMedicamento["idMedicamento_id"])
                    oMedicamento["nombre"]=medicamento.nombre
                print(ordenMedicamento)
            else:
                ordenMedicamento = list(OrdenMedicamento.objects.values())
                
            if len(ordenMedicamento)>0:
                message = "registros encontrados"
            else:
                message="registros no encontrados"
                status = 400
                raise Exception("Registros no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "OrdenesMedicamentos": ordenMedicamento}
        return JsonResponse(response,status=status)
    def put(self,request):
        pass
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ENF"])
            body = json.loads(request.body)
            idOrden = body["idOrden"]
            item = body["item"]
            IdMedicamento = body["IdMedicamento"]
            dosis = body["dosis"]
            tiempoTratamiento = body["tiempoTratamiento"]
            validadorMedicos.Dosis(dosis)
            medicamento = Medicamento.objects.get(IdMedicamento=IdMedicamento)
            orden = Orden.objects.get(idOrden=idOrden)
            ordenMedicamento_new = OrdenMedicamento(idOrden = orden,item = item,IdMedicamento = medicamento,dosis = dosis,tiempoTratamiento = tiempoTratamiento)
            ordenMedicamento_new.save()    
            message=" se registro la orden de Medicamento correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

class ConsultaMedica(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        pass
    def put(self,request):
        pass
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED"])
            body = json.loads(request.body)            
            idMascota = body["idMascota"]
            #cedulaMedico = body["cedulaMedico"]
            #fechaRegistro = body["fechaRegistro"]
            motivoConsulta = body["MotivoConsulta"]
            sintomas = body["Sintomas"]
            diagnostico = body["diagnostico"]
            medico= sesion.usuario
            #medico = PersonalClinica.objects.get(cedula=cedulaMedico)
            mascota = Mascota.objects.get(id=idMascota)
            fechaActual=str(datetime.now())
            fechaRegistro = date.today().strftime('%Y-%m-%d')
           #validaciones
            validadorMedicos.mConsulta(motivoConsulta)
            validadorMedicos.sintomas(sintomas)
            orden = Orden(idMascota=mascota,cedulaMedico=medico,fechaRegistro=fechaRegistro)
            orden.save()
            historiaActual={"fecha":fechaActual,
                "medico":str(medico.usuario)
                }
            historiaActual["MotivoConsulta"] = motivoConsulta
            historiaActual["Sintomas"] = sintomas
            historiaActual["Diagnostico"] = diagnostico
            historiaActual["idOrden"] = orden.id
            
            if ("medicamentos" in body or "procedimientos"in body) and "ayudasDiagnosticas" in body:
                orden.delete()
                raise Exception ("no se puede ordenar ayudas diagnosticas y medicamentos o procedimientos al tiempo")

            item = 0
            historiaActual["item"]={}
            try:  
                if "medicamentos" in body:
                    medicamentos = body["medicamentos"]
                    
                    for medicamento in medicamentos:
                        #Busco cual fue el ultimo ID de orden registrado
                        #idOrdenAnterior = Orden.objects.aggregate(Max('id'))['id__max']
                        #aumenta 1 para determinar cual es el siguiente ID de orden que se le va a asignar a esta orden
                        #idOrden = orden.id
                        #item = body["item"]
                        item +=1
                        idMedicamento = medicamento["idMedicamento"]
                        dosis = medicamento["dosis"]
                        tiempoTratamiento = medicamento["tiempoTratamiento"]
                        validadorMedicos.Dosis(dosis)
                        validadorMedicos.Tmedicamento(tiempoTratamiento)

                        #busca el medicamento con el id si no lo encuentra revienta 
                        medicamento = Medicamento.objects.get(idMedicamento=idMedicamento)
                        medicamentoHistoria={
                            "item": item,
                            "medicamento": medicamento.nombre,
                            "dosis": dosis,
                            "tiempoTratamiento":tiempoTratamiento                            
                        }
                        ordenMedicamento_new = OrdenMedicamento(idOrden = orden,item = item,idMedicamento = medicamento,dosis = dosis,tiempoTratamiento = tiempoTratamiento)
                        ordenMedicamento_new.save()  
                        historiaActual["item"][str(item)]=medicamentoHistoria
                        print("Se registro la OrdenMedicamento")  
            except Exception as error:
                orden.delete()
                print("Error en el primer try de Medicamento"+str(error))
                raise Exception(str(error))          
            
            try:
                if "procedimientos" in body:
                    procedimientos = body["procedimientos"]
                    for procedimiento in procedimientos:
                        #Busco cual fue el ultimo ID de orden registrado
                        #idOrdenAnterior = Orden.objects.aggregate(Max('id'))['id__max']
                        #aumenta 1 para determinar cual es el siguiente ID de orden que se le va a asignar a esta orden
                        #idOrden = orden.id
                        item +=1
                        idProcedimiento = procedimiento["idProcedimiento"]
                        cantidad = procedimiento["cantidad"]
                        asistenciaEspecializada = procedimiento["asistenciaEspecializada"]
                        validadorMedicos.Cantidad(cantidad)
                        procedimiento = Procedimiento.objects.get(codProcedimiento=idProcedimiento)
                        procedimientoHistoria={
                            "item": item,
                            "procedimiento": procedimiento.nombreProcedimiento,
                            "cantidad": cantidad,
                            "asistenciaEspecializada": asistenciaEspecializada                          
                        }
                        #revienta si no existe el procedimiento
                        ordenProcedimiento = OrdenProcedimiento(idOrden=orden,cantidad=cantidad,item= item,idProcedimiento=procedimiento,asistenciaEspecializada=asistenciaEspecializada)
                        ordenProcedimiento.save()
                        historiaActual["item"][str(item)]=procedimientoHistoria
            except Exception as error:
                print("Error en el primer try de procedimiento"+str(error))
                orden.delete()
                raise Exception(str(error))
            
            try:
                if "ayudasDiagnosticas" in body:
                    ayudaDiagnosticas = body["ayudasDiagnosticas"]
                    for ayuda in ayudaDiagnosticas:
                        item +=1
                        idAyuda = ayuda["ayuda"]
                        asistenciaEspecializada = ayuda["requiereEspecialista"]
                        cantidad = ayuda["cantidad"]
                        validadorMedicos.Cantidad(cantidad)
                        ayuda = Ayuda.objects.get(codAyuda=idAyuda)
                        ayudaHistoria={
                            "item": item,
                            "procedimiento": ayuda.nombreAyuda,
                            "cantidad": cantidad,
                            "asistenciaEspecializada": asistenciaEspecializada                          
                        }
                        ordenAyuda = OrdenAyudaDiagnostica(idOrden=orden,item= item,cantidad=cantidad,idAyuda=ayuda,asistenciaEspecializada=asistenciaEspecializada)
                        ordenAyuda.save()
                        historiaActual["item"][str(item)]=ayudaHistoria
            except Exception as error:
                print("Error en el primer try de AyudaDiagnostica"+str(error))
                orden.delete()
                raise Exception(str(error))
            
            #try:
            #    if "ayudaDiagnosticas" in body:
            #        print("entra")
            #        nombreAyuda = body["ayudaDiagnosticas"]["nombreAyuda"]
            #        cantidad = body["ayudaDiagnosticas"]["cantidad"]
            #        asistenciaEspecializada = body["ayudaDiagnosticas"]["asistenciaEspecializada"]
            #        ordenAyuda = OrdenAyudaDiagnostica(idOrden= orden,nombreAyuda=nombreAyuda,cantidad=cantidad,asistenciaEspecializada=asistenciaEspecializada)
            #        ordenAyuda.save()
            #        print("creada orden con id " +str(ordenAyuda.id))
            #except Exception as error:
            #    print("Error en el primer try de ayudaDiagnostica"+str(error))
            #    orden.delete()
            #    raise Exception(str(error))            

            #historia=collection.find_one({'_id': paciente.cedula})
            historia=collection.find_one({'_id': str(mascota.id)})
            historia["historias"][fechaActual]=historiaActual 
            collection.update_one({'_id': str(mascota.id)}, {'$set': historia})

            message="se agrego registro a historia clinica"
            message=" La historia de creo correctamente "
            status = 200        
        except Exception as error:
            #rden.delete()
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)
    
class ModuloProcedimiento(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=None):
        procedimientos = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ENF"])

            if id:
                procedimientos = list(Procedimiento.objects.filter(codProcedimiento=id).values())
            else:
                procedimientos = list(Procedimiento.objects.values())
                
            if len(procedimientos)>0:
                message = "registros encontrados"
            else:
                message="registros no encontrados"
                status = 400
                raise Exception("Registros no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Procedimientos": procedimientos}
        return JsonResponse(response,status=status)
    
    def put(self,request,id=None):
        pass
        
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED"])
            body = json.loads(request.body)

            nombreProcedimiento = body["nombreProcedimiento"]
            precio = body["precio"]
            validadorGeneral.validarNombre(nombreProcedimiento)

            procedimiento = Procedimiento(nombreProcedimiento = nombreProcedimiento,precio  = precio)
            procedimiento.save()    
            message=" El Procedimiento se registro correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

    def delete(self,request):
        pass

class ModuloOrdenProcedimiento(View):

    def get(self,request,id=None,cc=None):
        ordenProcedimiento = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ENF"])

            if id:
                #ordenMedicamento = OrdenMedicamento.objects.get(id=id)
                ordenProcedimiento = list(OrdenProcedimiento.objects.filter(id=id).values())
            elif cc:
                paciente = Mascota.objects.get(id=cc)            
                ordenePaciente = Orden.objects.get(cedulaPaciente=paciente.cedula,estado=1)
                ordenProcedimiento = list(OrdenProcedimiento.objects.filter(idOrden=ordenePaciente).values())
                for oProcedimiento in ordenProcedimiento:
                    nombreProcedimiento=Procedimiento.objects.get(codProcedimiento=oProcedimiento["idProcedimiento_id"])
                    oProcedimiento["nombre"]=nombreProcedimiento.nombreProcedimiento
                print(ordenProcedimiento)

            else:
                ordenProcedimiento = list(OrdenProcedimiento.objects.values())
                
            if len(ordenProcedimiento)>0:
                message = "registros encontrados"
            else:
                message="registros no encontrados"
                status = 400
                raise Exception("Registros no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
            print(str(error))
        response = {"message":message, "OrdenesProcedimientos": ordenProcedimiento}
        return JsonResponse(response,status=status)
    def put(self,request):
        pass
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED"])
            body = json.loads(request.body)
            idOrden = body["idOrden"]
            item = body["item"]
            codProcedimiento = body["codProcedimiento"]
            asistenciaEspecializada = body["asistenciaEspecializada"]
            #faltan los validadores de los otros campos

            #ordenMedicamento_new = OrdenMedicamento.objects.filter()
            #if seguro_new.exists():
            #    raise Exception("Ya Existe un Seguro con este ID")
            procedimiento = Procedimiento.objects.get(codProcedimiento=codProcedimiento)
            orden = Orden.objects.get(idOrden=idOrden)

            ordenProcedimiento_new = OrdenProcedimiento(idOrden = orden,item = item,idProcedimiento = procedimiento,asistenciaEspecializada = asistenciaEspecializada)
            ordenProcedimiento_new.save()    
            message=" se registro la orden de Procedimiento correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

class ModuloAyuda(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=None):
        ayudas = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ENF"])

            if id:
                ayudas = list(Ayuda.objects.filter(codAyuda=id).values())
            else:
                ayudas = list(Ayuda.objects.values())
                
            if len(ayudas)>0:
                message = "Ayudas encontrados"
            else:
                message="Ayudas no encontrados"
                status = 400
                raise Exception("Registros no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Ayudas": ayudas}
        return JsonResponse(response,status=status)
    
    def put(self,request,id=None):
        pass
        
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED"])
            body = json.loads(request.body)

            nombreProcedimiento = body["nombreProcedimiento"]
            precio = body["precio"]
            validadorGeneral.validarNombre(nombreProcedimiento)

            procedimiento = Procedimiento(nombreProcedimiento = nombreProcedimiento,precio  = precio)
            procedimiento.save()    
            message=" El Procedimiento se registro correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

    def delete(self,request):
        pass

class ModuloOrdenAyudaDiagnostica(View):
    def get(self,request):
        pass
    def put(self,request):
        pass
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED"])
            body = json.loads(request.body)
            idOrden = body["idOrden"]
            nombreAyuda = body["nombreAyuda"]
            cantidad = body["cantidad"]
            asistenciaEspecializada = body["asistenciaEspecializada"]
    
            orden = Orden.objects.get(idOrden=idOrden)

            ordenAyuda_new = OrdenAyudaDiagnostica(idOrden=orden,nombreAyuda=nombreAyuda,cantidad=cantidad,asistenciaEspecializada=asistenciaEspecializada)
            ordenAyuda_new.save()
            message=" se registro la orden de Procedimiento correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

    

    