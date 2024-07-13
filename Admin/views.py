from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from rest_framework import viewsets
from .serializers import AdminSerializer
from Asistencia.models import TrsAsistencia
from Asistencia.serializers import AsistenciaSerializer
from Participantes.serializers import ParticipanteSerializer
from Ponencia.serializers import PonenciasSerializer
from Admin.models import MaeAdministrador
from Participantes.models import MaeParticipantes
from Bloque.models import MaeBloque
from Bloque.serializers import BloqueSerializer
from Ponencia.models import MaePonencia
from Dia.models import MaeDia



class adminView(viewsets.ViewSet):
    queryset = MaeAdministrador.objects.all()
    serializer_class = AdminSerializer

    def index(self, request):
        contexto = {
            'mensaje': 'Error en la pagina'
        }
        return render(request, 'interfazAdmin.html', contexto)


    def generar_reporte(self, request):
        return render(request, 'pages/generarReporte.html', {'current_page': 'generar_reportes'})
    def registrar_ponentes(self, request):
        return render(request, 'pages/registrarPonente.html', {'current_page': 'registrar_ponentes'})
    def registrar_bloques(self, request):
        return render(request, 'pages/registrarBloques.html', {'current_page': 'registrar_bloques'})
    def registrar_ponencia(self, request):
        return render(request, 'pages/registrarPonencia.html', {'current_page': 'registrar_ponencia'})
    def registrar_universidades(self, request):
        return render(request, 'pages/registrarUniversidades.html', {'current_page': 'registrar_universidades'})

    def cerrar_sesion(request):
        return render(request, 'loginAdmin.html', {'current_page': 'cerrar_sesion'})
    

def ingresoAdmin(request):
    correoAdmin = request.POST.get('correo')
    contraseniaAdmin = request.POST.get('contrasenia')
    try:
        admin = MaeAdministrador.objects.get(correo=correoAdmin, contrasenia=contraseniaAdmin)
        request.session['correoAdmin'] = correoAdmin
        request.session['contraseniaAdmin'] = contraseniaAdmin
        serializer = AdminSerializer(admin)
        return render(request, 'interfazAdmin.html', serializer.data)
    except MaeAdministrador.DoesNotExist:
        print("No existe chavo")
        return redirect(reverse('LoguingAdministrador') + '?error=Usuario-o-contraseña-incorrectos')
    


def generar_reporte_documento(request):
    admin = TrsAsistencia.objects.all()
    
    asistencia = AsistenciaSerializer(admin, many=True)
    print('Participantes: ', asistencia.data)
    return JsonResponse({'success': True, 'data': asistencia.data})
    
    # admin2=MaePonencia.objects.all()
    # Ponen = PonenciasSerializer(admin2)
    # print(Ponen['nombre'])

    # admin3=MaeBloque.objects.all()
    # Bloq = BloqueSerializer(admin3)
    # print(Bloq['horainicio'].value,['horaFin'].value,['direccion'].value)





        