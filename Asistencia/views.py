from rest_framework import viewsets, permissions, response, status
from .models import TrsAsistencia
from .serializers import AsistenciaSerializer
from rest_framework.decorators import action

# Create your views here.
class viewAsistencias(viewsets.ModelViewSet):
    queryset = TrsAsistencia.objects.all()
    serializer_class = AsistenciaSerializer
