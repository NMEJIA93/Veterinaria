from django.shortcuts import render, redirect
from veterinariaApp.models import Sesion
from django.contrib import messages
import json
import random
import requests
from datetime import datetime

# Create your views here.
def login(request):  
    try:
        api_url="http://127.0.0.1:8000/logueo"
        print (request.GET)
        datos={"rol":request.GET["rol"],
            "usuario":request.GET["usuario"],
            "contraseña":request.GET["password"]
            }
        respuesta=requests.post(api_url, json=datos)
        response=json.loads(respuesta.text)
        print(respuesta.text)
        print(response["message"])
        print(respuesta.status_code)
        if respuesta.status_code==200:
            id= random.randint(100, 99999)
            ses=Sesion(id=id, token=response["token"])
            ses.save()
            redireccion="/" + datos["rol"]+"/"+str(ses.id)
            return redirect(redireccion)
        else:
            raise Exception(str(response["message"]))    
    except Exception as error:
        return render(request,'error_template.html',{'error_message':str(error)}) 

def renderLogin(request):
    return render(request, 'login.html')

def salir(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta=requests.delete(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(respuesta.text)
        print(response["message"])
        print(respuesta.status_code)
        if respuesta.status_code==200:
            return render(request, 'login.html')
        else:
            raise Exception(str(response["message"]))    
    except Exception as error:
        raise Exception(str(error))
#falta la ruta para los mensajes de error
def error_view(request, error_message, id):
    return render(request, 'error_template.html', {'error_message': error_message}, {'id':id})

def renderError(request,id=None):
    try:#voy a usar este
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response["rol"])
        redireccion="/" + response["rol"]+"/"+ id
        return redirect(redireccion)
    except Exception as error:
        if id==None:
            return render(request, 'login.html')
        else:
            error_message="Error en view front en def renderError: "+str(error)
            return render(request,'error_template.html',{'id':id,"error_message" : error_message})
        
#acciones con el rol ADM Administrativo
def renderAdministrativo(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["rol"] != "ADM":
            print("Enviar Error ")
            raise Exception("rol no valido")  
        return render(request,'administrador.html',{'id':id})
    except Exception as error:
        error_message="Error en view front en def renderAdministrador: "+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})


def renderRegistrarMascota(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        print(ses.token)
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response["rol"])
        if response["rol"] != "ADM":
            print("Enviar Error ")
            print("\nError en view front en def renderRegistrarPaciente\n")
            raise Exception("rol no valido")     
        return render(request,'registrarPaciente.html',{'id':id})
    except Exception as error:
        error_message="\nError en view front en def renderRegistrarPaciente\n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})  

def RegistrarMascota(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}   
        api_url="http://127.0.0.1:8000/paciente"
        fechanace = request.GET["fechanace"]
        fecha_obj = datetime.strptime(fechanace, '%Y-%m-%d')
        fechanace = fecha_obj.strftime('%d/%m/%Y')
        print(fechanace)
        print (request.GET)
        datos={"cedula":request.GET["cedulaPaciente"],
            "nombre":request.GET["nombre"],
            "genero":request.GET["genero"],
            "fechanace":str(fechanace),
            "telefono":request.GET["telefono"],
            "direccion":request.GET["direccion"],
            "email":request.GET["email"],
            "nombreContacto":request.GET["ncontacto"],
            "relacion":request.GET["pariente"],
            "telefonocontacto":request.GET["telefonoc"]
            }
        respuesta=requests.post(api_url, json=datos,headers=headers)
        response=json.loads(respuesta.text)
        print(respuesta.text)
        print(response["message"])
        print(respuesta.status_code)
        if respuesta.status_code==200:
            messages.add_message(request, messages.SUCCESS, "Paciente registrado")
            return render(request,'administrador.html',{'id':id})
        else:
            print("\nError en view front en def RegistrarPaciente\n")
            raise Exception(str(response["message"]))        
    except Exception as error:
        error_message="\nError en view front en def RegistrarPaciente\n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})  

def renderBuscaMascota(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["rol"] != "ADM":
            print("Enviar Error ")
            raise Exception("rol no valido")  
        return render(request,'buscaPaciente.html',{'id':id})
    except Exception as error:
        error_message="\nError en view front en def renderBuscaPaciente\n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})  

def BuscarPaciente(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}         
        api_url="http://127.0.0.1:8000/paciente/"+ request.GET["cedula"]
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["Pacientes"]:
            print(response["Pacientes"])
            messages.add_message(request, messages.SUCCESS, "Paciente Encontrado")
            return render(request, 'actualizarPaciente.html',{"id":id,"personas":response["Pacientes"]})
        raise Exception(response["message"])
    except Exception as error:
        error_message="\nError en view front en def BuscarPaciente: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})     

def ActualizarPaciente(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}   
        api_url="http://127.0.0.1:8000/paciente" 
        fechanace = request.GET["fechanace"]
        fecha_obj = datetime.strptime(fechanace, '%Y-%m-%d')
        fechanace = fecha_obj.strftime('%d/%m/%Y')
        print (request.GET)
        datos={"cedula":request.GET["cedula"],
            "nombre":request.GET["nombre"],
            "genero":request.GET["genero"],
            "fechanace":str(fechanace),
            "telefono":request.GET["telefono"],
            "direccion":request.GET["direccion"],
            "email":request.GET["email"]
            }
        respuesta=requests.put(api_url, json=datos,headers=headers)
        response=json.loads(respuesta.text)
        print(respuesta.text)
        print(response["message"])
        print(respuesta.status_code)
        if respuesta.status_code==200:
            messages.add_message(request, messages.SUCCESS, "Paciente actualizado")
            return render(request,'administrador.html',{'id':id})
        else:
            raise Exception(str(response["message"]))         
    except Exception as error:
        error_message="\nError en view front en def ActualizarPaciente: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def renderActualizarPaciente(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["rol"] != "ADM":
            print("Enviar Error ")
            raise Exception("rol no valido")  
        return render(request,'buscaPaciente.html',{'id':id})
    except Exception as error:
        error_message="\nError en view front en def renderActualizarPaciente: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def renderContactoPaciente(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["rol"] != "ADM":
            print("Enviar Error ")
            raise Exception("rol no valido")  
        return render(request,'contactoPaciente.html',{'id':id})
    except Exception as error:
        error_message="\nError en view front en def renderContactoPaciente: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})
    
def RegistrarContacto(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}   
        api_url="http://127.0.0.1:8000/contactoPaciente"
        print (request.GET)
        datos={"paciente":request.GET["cedula"],
            "nombre":request.GET["nombreC"],
            "relacion":request.GET["pariente"],
            "telefono":request.GET["telefonoc"]            
            }
        respuesta=requests.post(api_url, json=datos,headers=headers)
        response=json.loads(respuesta.text)
        print(respuesta.text)
        print(response["message"])
        print(respuesta.status_code)
        if respuesta.status_code==200:
            return render(request,'administrador.html',{'id':id})
        else:
            raise Exception(str(response["message"]))        
    except Exception as error:
        error_message="\nError en view front en def RegistrarContacto: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def BuscarContactoP(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}    
        api_url="http://127.0.0.1:8000/paciente/"+ request.GET["cedula"]
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["Pacientes"]:
            print(response["Pacientes"])
            messages.add_message(request, messages.SUCCESS, "Paciente Encontrado")
            return render(request, 'contactoPaciente.html',{"id":id,"personas":response["Pacientes"]})
        raise Exception(response["message"])
    except Exception as error:
        error_message="\nError en view front en def BuscarContactoP: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def renderbuscaContacto(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["rol"] != "ADM":
            print("Enviar Error ")
            raise Exception("rol no valido")  
        return render(request,'buscaContacto.html',{'id':id})
    except Exception as error:
        error_message="Error en view front en def renderbuscaContacto: "+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})  

def renderPoliza(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["rol"] != "ADM":
            print("Enviar Error ")
            raise Exception("rol no valido")  
        return render(request,'poliza.html',{'id':id})
    except Exception as error:
        error_message="\nError en view front en def renderPoliza: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def BuscarPacienteP(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}         
        api_url="http://127.0.0.1:8000/paciente/"+ request.GET["cedula"]
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["Pacientes"]:
            print(response["Pacientes"])
            messages.add_message(request, messages.SUCCESS, "Paciente Encontrado")
            return render(request, 'poliza.html',{"id":id,"personas":response["Pacientes"]})
        raise Exception(response["message"])
    except Exception as error:
        error_message="\nError en view front en def BuscarPacienteP: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def renderbuscaPoliza(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["rol"] != "ADM":
            print("Enviar Error ")
            raise Exception("rol no valido")  
        return render(request,'buscaPoliza.html',{'id':id})
    except Exception as error:
        error_message="\nError en view front en def renderbuscaPoliza: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def BuscarPoliza(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}    
        api_url="http://127.0.0.1:8000/paciente/"+ request.GET["cedula"]
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["Pacientes"]:
            print(response["Pacientes"])
            messages.add_message(request, messages.SUCCESS, "Paciente Encontrado")
            return render(request, 'poliza.html',{"id":id,"personas":response["Pacientes"]})
        raise Exception(response["message"])
    except Exception as error:
        error_message="\nError en view front en def BuscarPoliza: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def RegistraPoliza(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}   
        api_url="http://127.0.0.1:8000/seguropaciente"
        print (request.GET)        
        fechaVigencia = request.GET["vigencia"]
        fecha_obj = datetime.strptime(fechaVigencia, '%Y-%m-%d')
        fechaVigencia = fecha_obj.strftime('%d/%m/%Y')
        print(fechaVigencia)
        datos={"idSeguro":request.GET["poliza"],
            "nombreAseguradora":request.GET["aseguradora"],
            "vigencia":str(fechaVigencia),
            "estado":"1",
            "paciente":request.GET["cedula"]
            }
        respuesta=requests.post(api_url, json=datos,headers=headers)
        response=json.loads(respuesta.text)
        print(respuesta.text)
        print(response["message"])
        print(respuesta.status_code)
        if respuesta.status_code==200:
            messages.add_message(request, messages.SUCCESS, "Poliza del Paciente registrada")
            return render(request,'administrador.html',{'id':id})
        else:
            raise Exception(str(response["message"]))        
    except Exception as error:
        error_message="\nError en view front en def RegistraPoliza: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})
    
#acciones con el rol RH
def renderRH(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response["rol"])
        if response["rol"] != "RH":
            print("Enviar Error ")
            raise Exception("Tu rol debe ser RH")          
        return render(request,'personalClinica.html',{'id':id})
    except Exception as error:
        error_message="\nError en view front en def renderRH: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def renderRegistrarEmpleado(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response["rol"])
        if response["rol"] != "RH":
            raise Exception("Tu rol debe ser RH")          
        return render(request,'registrarEmpleado.html',{'id':id})
    except Exception as error:
        error_message="\nError en view front en def renderRegistrarEmpleado: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def RegistrarEmpleado(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}   
        api_url="http://127.0.0.1:8000/usuarioClinica"
        fechanace = request.GET["fechanace"]
        fecha_obj = datetime.strptime(fechanace, '%Y-%m-%d')
        fechanace = fecha_obj.strftime('%d/%m/%Y')
        print(fechanace)
        print (request.GET)
        datos={"cedula":request.GET["cedula"],
            "nombre":request.GET["nombre"],
            "fechanace":str(fechanace),
            "telefono":request.GET["telefono"],
            "direccion":request.GET["direccion"],
            "email":request.GET["email"],
            "rol":request.GET["rol"],
            "usuario":request.GET["usuario"],
            "password":request.GET["password"]
            }
        respuesta=requests.post(api_url, json=datos,headers=headers)
        response=json.loads(respuesta.text)
        print(respuesta.text)
        print(response["message"])
        print(respuesta.status_code)
        if respuesta.status_code==200:
            messages.add_message(request, messages.SUCCESS, "Empleado registrado")
            return render(request,'personalClinica.html',{'id':id})
        else:
            raise Exception(str(response["message"]))        
    except Exception as error:
        error_message="\nError en view front en def RegistrarEmpleado: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def renderBuscaEmpleado(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response["rol"])
        if response["rol"] != "RH":
            print("Enviar Error ")
            raise Exception("Tu rol debe ser RH")          
        return render(request,'buscaEmpleado.html',{'id':id})
    except Exception as error:
        error_message="\nError en view front en def renderBuscaEmpleado: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def BuscarEmpleado(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}  
        dato=request.GET["cedula"]       
        api_url="http://127.0.0.1:8000/usuarioClinica/"+ str(dato)
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["Empleados"]:
            print(response["Empleados"])
            messages.add_message(request, messages.SUCCESS, "Empleado Encontrado")
            return render(request, 'actualizarEmpleado.html',{"id":id,"personas":response["Empleados"]})
        raise Exception(response["message"])
    except Exception as error:
        error_message="\nError en view front en def BuscarEmpleado: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def renderActualizarEmpleado(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response["rol"])
        if response["rol"] != "RH":
            print("Enviar Error ")
            raise Exception("Tu rol debe ser RH")          
        return render(request,'buscaEmpleado.html',{'id':id})
    except Exception as error:
        error_message="\nError en view front en def renderActualizarEmpleado: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def ActualizarEmpleado(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}   
        api_url="http://127.0.0.1:8000/usuarioClinica"
        fechanace = request.GET["fechanace"]
        fecha_obj = datetime.strptime(fechanace, '%Y-%m-%d')
        fechanace = fecha_obj.strftime('%d/%m/%Y')
        print(fechanace)
        print (request.GET)
        datos={"cedula":request.GET["cedula"],
            "nombre":request.GET["nombre"],
            "fechanace":str(fechanace),
            "telefono":request.GET["telefono"],
            "direccion":request.GET["direccion"],
            "email":request.GET["email"],
            "rol":request.GET["rol"],
            "usuario":request.GET["usuario"],
            "password":request.GET["password"]
            }
        respuesta=requests.put(api_url, json=datos,headers=headers)
        response=json.loads(respuesta.text)
        print(respuesta.text)
        print(response["message"])
        print(respuesta.status_code)
        if respuesta.status_code==200:
            messages.add_message(request, messages.SUCCESS, "Empleado actualizado")
            return render(request,'personalClinica.html',{'id':id})
        else:
            raise Exception(str(response["message"]))        
    except Exception as error:
        error_message="\nError en view front en def ActualizarEmpleado: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def renderInactivarEmpleado(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response["rol"])
        if response["rol"] != "RH":
            print("Enviar Error ")
            raise Exception("Tu rol debe ser RH")          
        return render(request,'inactivarEmpleado.html',{'id':id})
    except Exception as error:
        error_message="\nError en view front en def renderInactivarEmpleado: \n"+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def BuscarInactivar(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}         
        api_url="http://127.0.0.1:8000/usuarioClinica/"+ request.GET["cedula"]
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(respuesta.status_code)
        if respuesta.status_code==200:
            messages.add_message(request, messages.SUCCESS, "Empleado Encontrado")
            return render(request, 'inactivarEmpleado.html',{'id':id, "personas":response["Empleados"]} )
        raise Exception(response["message"])
    except Exception as error:
        error_message="Error en view front en def BuscarInactivar: "+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def InactivarEmpleado(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}  
        print(request.GET["cedula1"])
        api_url="http://127.0.0.1:8000/usuarioClinica/"+ request.GET["cedula1"]
        respuesta = requests.delete(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if respuesta.status_code==200:
            messages.add_message(request, messages.SUCCESS, "Empleado Inactivo")
            return render(request, 'personalClinica.html',{'id':id})
        else:
            raise Exception(str(response["message"]))    
    except Exception as error:
        error_message="Error en view front en def InactivarEmpleado: "+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def renderLicenciaEmpleado(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response["rol"])
        if response["rol"] != "RH":
            print("Enviar Error ")
            raise Exception("Tu rol debe ser RH")          
        return render(request,'licenciaEmpleado.html',{'id':id})
    except Exception as error:
        error_message="Error en view front en def renderLicenciaEmpleado: "+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def renderBuscaEmpleadoN(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'token': str(ses.token)}
        api_url="http://127.0.0.1:8000/logueo"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response["rol"])
        if response["rol"] != "RH":
            print("Enviar Error ")
            raise Exception("Tu rol debe ser RH")          
        return render(request,'buscaEmpleadoN.html',{'id':id})
    except Exception as error:
        error_message="Error en view front en def renderBuscaEmpleadoN: "+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def BuscarEmpleadoN(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}  
        dato=request.GET["cedula"]
        api_url="http://127.0.0.1:8000/usuarioClinica/"+ str(dato)
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["Empleados"]:
            print(response["Empleados"])
            messages.add_message(request, messages.SUCCESS, "Empleado Encontrado")
            return render(request, 'licenciaEmpleado.html',{"id":id,"personas":response["Empleados"]})
        raise Exception(response["message"])
    except Exception as error:
        error_message="Error en view front en def BuscarEmpleadoN: "+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})

def licenciaEmpleado(request, id):
    try: 
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}   
        fechareg = datetime.now()
        print (fechareg)
        fechareg = fechareg.strftime('%d/%m/%Y')
        api_url="http://127.0.0.1:8000/novedades"
        print (request.GET)
        datos={"cedula":request.GET["cedula"],
            "tipo":request.GET["novedad"],
            "tiempo":request.GET["tiempo"],
            "fechaRegistro":str(fechareg),
            "observaciones":request.GET["observa"]
            }
        respuesta=requests.post(api_url, json=datos,headers=headers)
        response=json.loads(respuesta.text)
        print(respuesta.text)
        print(response["message"])
        print(respuesta.status_code)
        if respuesta.status_code==200:
            messages.add_message(request, messages.SUCCESS, "Novedad registrado")
            return render(request,'personalClinica.html',{'id':id})
        else:
            raise Exception(str(response["message"]))        
    except Exception as error:
        error_message="Error en view front en def licenciaEmpleado: "+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})
        #raise Exception(str(error))

def renderMuestraEmpleado(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}   
        api_url="http://127.0.0.1:8000/usuarioClinica"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        print(response)
        if response["Empleados"]:
            print(response["Empleados"])
            messages.add_message(request, messages.SUCCESS, "Listado de Empleados")
            return render(request, 'muestraEmpleado.html',{"id":id,"personas":response["Empleados"]})
        raise Exception(response["message"])
    except Exception as error:
        error_message="Error en view front en def renderMuestraEmpleado: "+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})
        #raise Exception(str(error))

def renderAsistencias(request, id):
    try:
        ses=Sesion.objects.get(id=id)
        headers={'TOKEN': str(ses.token)}   
        api_url="http://127.0.0.1:8000/asistencias"
        respuesta = requests.get(api_url, headers=headers)
        response=json.loads(respuesta.text)
        if response["Asistencias"]:
            print(response["Asistencias"])
            return render(request, 'asistencias.html',{"id":id,"personas":response["Asistencias"]})
        raise Exception(response["message"])
    except Exception as error:
        error_message="Error en view front en def renderAsistencias: "+str(error)
        return render(request,'error_template.html',{'id':id,"error_message" : error_message})
