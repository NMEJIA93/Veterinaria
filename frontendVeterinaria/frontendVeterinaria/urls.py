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
    renderPoliza,
    renderbuscaPoliza,
    BuscarPoliza,
    RegistraPoliza,
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
    # path ('contactoPaciente/<id>', renderContactoPaciente),
    # path ('buscaContacto/<id>', renderbuscaContacto),
    # path ('contactoPaciente1/<id>', RegistrarContacto),
    # path ('buscaContactoP/<id>', BuscarContactoP),
    # path ('poliza/<id>', renderPoliza),
    # path ('buscaPoliza/<id>', renderbuscaPoliza),
    # path ('poliza1/<id>', BuscarPoliza),
    # path ('poliza2/<id>', RegistraPoliza)
]
