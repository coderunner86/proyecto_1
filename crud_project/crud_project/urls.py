"""
URL configuration for crud_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from usuarios.views import (
    crear_usuario,
    listar_usuarios,
    obtener_usuario,
    eliminar_usuario,
    geocodificar_base,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('crear/', crear_usuario, name='crear_usuario'),
    path('lista/', listar_usuarios, name='lista_usuarios'),
    path('usuario/<int:id>/', obtener_usuario, name='obtener_usuario'),
    path('eliminar/<int:id>/', eliminar_usuario, name='eliminar_usuario'),
    path('geocodificar_base/', geocodificar_base, name='geocodificar_base'),
]
