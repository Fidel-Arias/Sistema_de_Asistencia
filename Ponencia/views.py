from django.shortcuts import render
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import MaePonencia
from Bloque.models import MaeBloque
from .serializers import PonenciasSerializer

# Create your views here.
class viewPonencias(viewsets.ModelViewSet):
    queryset = MaePonencia.objects.all()
    serializer_class = PonenciasSerializer

    @method_decorator(login_required)
    def verPonencias(self, request):
        bloques = MaeBloque.objects.filter().order_by('iddia__fecha')
        return render(request, 'ponencias.html', {'ponencias': bloques})
    
    @method_decorator(login_required)
    def regresar_perfil(self, request):
        return render(request, 'participante.html')