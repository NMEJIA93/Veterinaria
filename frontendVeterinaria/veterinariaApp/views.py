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
        

