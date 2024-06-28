from django.shortcuts import render, redirect
from rest_framework import viewsets
from .serializers import AdminSerializer
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
    

def ingresoAdmin(request, correo, pk):
    try:
        admin = MaeAdministrador.objects.get(correo=correo, contrasenia=pk)
    except MaeAdministrador.DoesNotExist:
        print("No existe chavo")
        return render(request, 'login.html', {'current_page': 'error_admin'})
    serializer = AdminSerializer(admin)
    print("validacion: ", request.session.get('contrasenia'))
    return render(request, 'interfazAdmin.html', serializer.data)


def generar_reporte_documento(self, request):
    admin = MaeParticipantes.objects.all()
    
    parti = ParticipanteSerializer(admin)
    print(parti['codParticipante'].value, {'apellido'}.value,['email'].value)
    
    admin2=MaePonencia.objects.all()
    Ponen = PonenciasSerializer(admin2)
    print(Ponen['nombre'])

    admin3=MaeBloque.objects.all()
    Bloq = BloqueSerializer(admin3)
    print(Bloq['horainicio'].value,['horaFin'].value,['direccion'].value)





        