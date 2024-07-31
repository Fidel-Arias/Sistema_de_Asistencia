from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Admin.models import MaeAdministrador

@login_required
def interfaz_administrador(request):
    correo = request.session.get('correo_admin')
    contrasenia = request.session.get('contrasenia_admin')
    admin = MaeAdministrador.objects.get(correo=correo, contrasenia=contrasenia)
    return render(request, 'interfazBienvenida.html', {'admin': admin})