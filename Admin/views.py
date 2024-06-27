from django.shortcuts import render, redirect
from rest_framework import viewsets
from .serializers import AdminSerializer
from .models import MaeAdministrador

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