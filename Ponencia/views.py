from django.shortcuts import render
from rest_framework import viewsets, permissions, response, status
from .models import MaePonencia
from .serializers import PonenciasSerializer

# Create your views here.
class viewPonencias(viewsets.ModelViewSet):
    queryset = MaePonencia.objects.all()
    serializer_class = PonenciasSerializer

    def verPonencias(self, request):
        codigo = request.session.get('codigo', None)
        print('Codigo ver: ', codigo)
        print('JSON: ', self.queryset)
        return render(request, 'ponencias.html', {'ponencias': self.queryset, 'codigo': codigo})