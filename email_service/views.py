from config import settings
from rest_framework.request import HttpRequest
from django.core.signing import TimestampSigner
from rest_framework import status
from django.core.mail import send_mail, get_connection, BadHeaderError
from django.template.loader import render_to_string
from premailer import transform
import json


# Create your views here.
def email_service(request, formulario_data):

    # Generar token de validacion
    token_generator = generar_token(formulario_data)
    print('token: ', token_generator)

    # Configurando dinámicamente el email_host_user y el email_host_password
    settings.EMAIL_HOST_USER = formulario_data['correo']
    settings.EMAIL_HOST_PASSWORD = formulario_data['contrasenia']

    # Crear una nueva conexión SMTP con las credenciales dinámicas
    connection = get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS,
    )
    
    template = render_to_string('mail_context.html', {
        'nombre_admin': f"{formulario_data['nombres']} {formulario_data['apellidos']}",
        'nombre_congreso': formulario_data['nombreCongreso'],
        'correo': formulario_data['correo'],
        'protocolo': request.scheme,
        'dominio': request.get_host(),
        'token': token_generator
    })

    template = transform(template)
    plain_message = f'Nuevo administrador: {formulario_data['nombres']} {formulario_data['apellidos']}\nCongreso: {formulario_data['nombreCongreso']}\nCorreo: {formulario_data['correo']}\nValida el registro aquí: {token_generator}'

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

        # Cerrar la conexión SMTP
        connection.close()
        
        return 'success'
    except BadHeaderError:
        print("Encabezado inválido.")
        return 'failed'
    except Exception as e:
        print("Error SMTP: ", e)
        return 'failed'
    
def generar_token(data):
    signer = TimestampSigner()
    data_serializado = json.dumps(data)
    token = signer.sign(data_serializado)
    return token