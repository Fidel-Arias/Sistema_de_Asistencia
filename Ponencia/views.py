from django.shortcuts import render
from rest_framework import viewsets, permissions, response, status
from .models import MaePonencia
from .serializers import PonenciasSerializer

# Create your views here.
class viewPonencias(viewsets.ModelViewSet):
    queryset = MaePonencia.objects.all()
    serializer_class = PonenciasSerializer

    def verPonencias(self, request):
        ponencias = MaePonencia.objects.all()
        return render(request, 'ponencias.html', {'ponencias': ponencias})
    def regresar_perfil(self, request):
        return render(request, 'participante.html')