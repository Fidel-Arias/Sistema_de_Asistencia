from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ColaboradorSerializer
from .models import MaeColaborador

# Create your views here.
class Colaborador(viewsets.ViewSet):
    queryset = MaeColaborador.objects.all()
    serializer_class = ColaboradorSerializer

    def ingresoColaborador(request, correo, pk):
        try:
            colaborador = MaeColaborador.objects.get(correo=correo, contrasenia=pk)
        except MaeColaborador.DoesNotExist:
            print("No existe chavo")
            return render(request, 'loginColaborador.html', {'current_page': 'error_admin'})
        serializer = ColaboradorSerializer(colaborador)
        print("validacion: ", request.session.get('contrasenia'))
        return render(request, 'colaborador.html', serializer.data)

    