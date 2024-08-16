from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from Congreso.models import MaeCongreso
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from Congreso.nuevo_congreso import creando_nuevo_congreso
from Admin.models import MaeAdministrador

def activar_admin(request, uidb64, token, formulario):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        usuario = MaeAdministrador.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, MaeAdministrador.DoesNotExist):
        usuario = None

    if usuario is not None and default_token_generator.check_token(usuario, token):
        creando_nuevo_congreso(formulario)
        usuario.idcongreso=MaeCongreso.objects.get(nombre=formulario['nombreCongreso'])  # El id del congreso debe ser dinámico según el cargado en la base de datos.
        usuario.save()
        return HttpResponse('El registro del administrador ha sido validado exitosamente.')
    else:
        return HttpResponse('El enlace de activación no es válido o ha expirado.')