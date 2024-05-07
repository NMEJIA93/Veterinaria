"""backendVeterinaria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from veterinariaApp.views import Logueo
from veterinariaApp.views import Propietario
from veterinariaApp.views import ModuloMascota
from veterinariaApp.views import ModuloPersonalClinica

from veterinariaApp.views import ConsultaMedica,ModuloMedicamento,ModuloOrdenMedicamento, Procedimiento
from veterinariaApp.views import ModuloOrdenProcedimiento, ModuloAyuda, ModuloProcedimiento


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logueo',Logueo.as_view(),name="login"),
    path('propietario',Propietario.as_view(),name="Modulo propietario"),
    path('propietario/<id>',Propietario.as_view(),name="Modulo propietario"),
    path('mascota',ModuloMascota.as_view(),name="Modulo Mascota"),
    path('mascota/<id>',ModuloMascota.as_view(),name="Modulo Mascota"),
    path('usuarioClinica',ModuloPersonalClinica.as_view(),name="modulo usuario Recursos Humanos"),
    path('usuarioClinica/<id>',ModuloPersonalClinica.as_view(),name="Busca_empleado"),
    path('medicamento', ModuloMedicamento.as_view(), name='modulo Medico Mediicamento'), 
    path('medicamento/<id>', ModuloMedicamento.as_view(), name='modulo Medico Mediicamento'),
    path('procedimiento', ModuloProcedimiento.as_view(), name='moduloprocedimientos'), 
    path('procedimiento/<id>', ModuloProcedimiento.as_view(), name='moduloprocedimientos'),
    path('ayuda', ModuloAyuda.as_view(), name='ayudas'),
    path('ayuda/<id>', ModuloAyuda.as_view(), name='ayudas'),
    path('ordenmedicamento', ModuloOrdenMedicamento.as_view(), name='Modulo ModuloOrdenMedicamento'), 
    path('ordenmedicamento/<id>', ModuloOrdenMedicamento.as_view(), name='Modulo ModuloOrdenMedicamento'), 
    path('ordenmedicamento/paciente/<cc>', ModuloOrdenMedicamento.as_view(), name='Modulo ModuloOrdenMedicamento'), 
    path('ordenmedicamento/<id>/<cc>', ModuloOrdenMedicamento.as_view(), name='modulo Medico Mediicamento'), 
    path('ordenprocedimiento/<id>', ModuloOrdenProcedimiento.as_view(), name='ordenprocedimiento'),
    path('ordenprocedimiento/paciente/<cc>', ModuloOrdenProcedimiento.as_view(), name='ordenprocedimiento'),
    path('consulta', ConsultaMedica.as_view(), name='modulo Medico HistoriaClinica'), 
    path('consulta/<id>', ConsultaMedica.as_view(), name='modulo  Medico HistoriaClinica'), 
]
