from Admin.models import AdminToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from rest_framework import status
from Admin.serializers import AdminSerializer
from Congreso.models import MaeCongreso
from tipoUsuario.models import MaeTipoUsuario
from Congreso.nuevo_congreso import creando_nuevo_congreso
import json

@api_view(['GET'])
def activar_admin(request): #Encriptar las contraseñas
    token = request.GET.get('token')
    print('token desde activar_admin: ', token)
    data = validar_token(token, max_age=3600)

    if data == status.HTTP_400_BAD_REQUEST:
        return HttpResponse("URL no válida", status=status.HTTP_400_BAD_REQUEST)

    is_valid = creando_nuevo_congreso(data)

    if is_valid == 'failed':
        return HttpResponse("Error al crear el congreso", status=status.HTTP_400_BAD_REQUEST)
    elif is_valid == 'exists':
        return HttpResponse("El congreso ya existe", status=status.HTTP_400_BAD_REQUEST)
    
    data['idtipo'] = MaeTipoUsuario.objects.get(dstipo="ADMINISTRADOR").pk
    data['idcongreso'] = MaeCongreso.objects.get(nombre=data['nombreCongreso']).pk
    serializer = AdminSerializer(data=data)

    if serializer.is_valid():
        admin = serializer.save()

        token = AdminToken.objects.create(admin=admin)

        html = """<html>
                    <body>
                        <h1>Administrador creado con exito</h1>
                        <p>Puede cerrar esta pestaña</p>
                    </body>
                </html>"""

        return HttpResponse(html, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def validar_token(token, max_age):
    signer = TimestampSigner()
    try:
        data = signer.unsign(token, max_age=max_age)
        data = json.loads(data)
        return data
    except (BadSignature, SignatureExpired, Exception ) as e:
        print('Error validando token: ', e)
        return status.HTTP_400_BAD_REQUEST