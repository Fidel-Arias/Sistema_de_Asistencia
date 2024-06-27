from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import UniversidadSerializer
from .models import MaeUniversidad

# Create your views here.

class UniversidadViewSet(viewsets.ModelViewSet):
    queryset = MaeUniversidad.objects.all()
    #permission_classes = [permissions.AllowAny] #SOLO ADMIN
    serializer_class = UniversidadSerializer