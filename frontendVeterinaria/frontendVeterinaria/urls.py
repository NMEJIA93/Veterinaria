"""frontendVeterinaria URL Configuration

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
from veterinariaApp.views import renderLogin, login, salir, renderError
from veterinariaApp.views import (
    renderAdministrativo,
    renderActualizarPaciente,
    renderRegistrarMascota,
    RegistrarMascota,
    ActualizarPaciente,
    renderBuscaMascota,
    BuscarMascota,
    renderContactoPaciente,
    renderbuscaContacto,
    RegistrarContacto,
    BuscarContactoP,
)
from veterinariaApp.views import (
    renderRH,
    renderRegistrarEmpleado,
    RegistrarEmpleado,
    renderBuscaEmpleado,
    BuscarEmpleado,
    renderActualizarEmpleado,
    ActualizarEmpleado,
    renderInactivarEmpleado,
    BuscarInactivar,
    InactivarEmpleado,
    renderBuscaEmpleadoN,
    BuscarEmpleadoN,
    renderMuestraEmpleado,
    renderMED,
    renderhistoriaClinica,
    BuscarPacienteH,
    RegistrarHistoriaClinica
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", renderLogin),
    path("login/", login),
    path("login/<id>", salir),
    path("error/", renderError),
    path("error/<id>", renderError),
    # rutas para el rol Auxiliar Administrativo
    path("ADM/<id>", renderAdministrativo),
    # path ('actualizarPaciente/<id>', renderActualizarPaciente),
    path("registrarMascota/<id>", renderRegistrarMascota),
    path("registrarMascota1/<id>", RegistrarMascota),
    # path ('actualizarPaciente1/<id>', ActualizarPaciente),
    path("buscaMascota/<id>", renderBuscaMascota),
    path("buscaMascota1/<id>", BuscarMascota),
    path ('contactoPaciente/<id>', renderContactoPaciente),
    path ('buscaContacto/<id>', renderbuscaContacto),
    path ('contactoPaciente1/<id>', RegistrarContacto),
    path ('buscaContactoP/<id>', BuscarContactoP),
    # rutas para el rol recursos humanos
    path("RH/<id>", renderRH),
    path("registrarEmpleado/<id>", renderRegistrarEmpleado),
    path("registrarEmpleado1/<id>", RegistrarEmpleado),
    path("buscaEmpleado/<id>", renderBuscaEmpleado),
    path("buscaEmpleado1/<id>", BuscarEmpleado),
    path("actualizarEmpleado/<id>", renderActualizarEmpleado),
    path("actualizarEmpleado1/<id>", ActualizarEmpleado),
    path("inactivarEmpleado/<id>", renderInactivarEmpleado),
    path("inactivarEmpleado1/<id>", BuscarInactivar),
    path("inactivarEmpleado2/<id>", InactivarEmpleado),
    path("buscaEmpleadoN/<id>", renderBuscaEmpleadoN),
    path("buscaEmpleadoN1/<id>", BuscarEmpleadoN),
    path("muestraEmpleado/<id>", renderMuestraEmpleado),
    #ruta para el rol de medico
    path('MED/<id>', renderMED),
    path('historiaClinica/<id>', renderhistoriaClinica),
    path('historiaClinica1/<id>', BuscarPacienteH),
    path('historiaClinica2/<id>', RegistrarHistoriaClinica),
]
