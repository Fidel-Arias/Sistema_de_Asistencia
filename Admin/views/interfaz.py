from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from django.shortcuts import render
from Admin.models import MaeAdministrador

class Interfaz_Administrador(viewsets.ViewSet):
    @method_decorator(login_required)
    def interfaz_administrador(self, request):
        correo = request.session.get('correo_admin')
        contrasenia = request.session.get('contrasenia_admin')
        admin = MaeAdministrador.objects.get(correo=correo, contrasenia=contrasenia)
        return render(request, 'interfazBienvenida.html', {'admin': admin})