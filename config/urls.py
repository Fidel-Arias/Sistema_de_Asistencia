"""
URL configuration for config project.

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
from Participantes.views import viewParticipantes

urlpatterns = [
    path('', include('Login.urls')),
    path('Administrador/', include('Admin.urls')),
    path('Colaborador/', include('Colaborador.urls')),
    path('Administrador/', include('Asistencia.urls')),
    path('user/', include('Ponencia.urls')),
    path('user/', include('Ponente.urls')),
    path('', include('Bloque.urls')),
    path('', include('Universidad.urls')),
    path('', include('Participantes.urls')),
    # path('participante', viewParticipantes.as_view({'get': 'list'})),
    # path('participante/<str:pk>', viewParticipantes.as_view({'get': 'retrieve'})),
]
 #    path('api/ponentes/<int:pk>', viewPonentes.as_view({'get': 'ponente'})), --------ejemplo --- no se modifica