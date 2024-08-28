from config import settings
from django.core.mail import send_mail, get_connection, BadHeaderError
from premailer import transform

# Create your views here.
def email_service(request, formulario_data, template, plain_message, subject, to_email):

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
    
    template = transform(template)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=template,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
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
    
