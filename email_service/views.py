from config import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from rest_framework import status
from django.core.mail import send_mail, get_connection, BadHeaderError
from django.template.loader import render_to_string
from premailer import transform
from Admin.models import MaeAdministrador
from tipoUsuario.models import MaeTipoUsuario
from Congreso.models import MaeCongreso


# Create your views here.
def email_service(request, formulario_data):
    nombres = formulario_data['nombresAdmin']
    apellidos = formulario_data['apellidosAdmin']
    correo = formulario_data['correoAdmin']
    contrasenia = formulario_data['contrasenaAdmin']
    nombre_congreso= formulario_data['nombreCongreso']
    tipo_usuario = MaeTipoUsuario.objects.get(dstipo='ADMINISTRADOR')
    

    # Configurando dinámicamente el email_host_user y el email_host_password
    settings.EMAIL_HOST_USER = correo
    settings.EMAIL_HOST_PASSWORD = contrasenia

    # Crear una nueva conexión SMTP con las credenciales dinámicas
    connection = get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS,
    )

    #Creando al administrador
    administrador = MaeAdministrador(
        nombres=nombres,
        apellidos=apellidos,
        correo=correo,
        contrasenia=contrasenia,
        idtipo=tipo_usuario.idtipo,
    )

    #Generar token de validacion
    token = default_token_generator.make_token(administrador)
    uid = urlsafe_base64_encode(force_bytes(administrador.pk))
    enlace_verificacion = reverse('activar_admin', kwargs={'uidb64': uid, 'token': token, 'formulario': formulario_data})
    url_completa = f'{request.scheme}://{request.get_host()}{enlace_verificacion}'

    template = render_to_string('mail_context.html', {
        'nombre_admin': nombres + ' ' + apellidos,
        'nombre_congreso': nombre_congreso,
        'correo': correo,
        'validation_link': url_completa
    })

    template = transform(template)
    plain_message = f'Nuevo administrador: {nombres} {apellidos}\nCongreso: {nombre_congreso}\nCorreo: {correo}\nValida el registro aquí: https://www.google.com/'

    try:
        send_mail(
            subject='Registro para administrador en Sistema de Asistencia JINIS',
            message=plain_message,
            html_message=template,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['fidel.arias@ucsm.edu.pe'],
            fail_silently=False,
            connection=connection,  # Utilizar la conexión con las nuevas credenciales
            
        )
        
        return 'success'
    except BadHeaderError:
        print("Encabezado inválido.")
        return 'failed'
    except Exception as e:
        print("Error SMTP: ", e)
        return 'failed'