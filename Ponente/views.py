from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import MaePonente
from .serializaers import PonentesSerializer
from rest_framework import response, status
from .serializaers import PonentesSerializer

# Create your views here.
class viewPonentes(viewsets.ModelViewSet):
    queryset = MaePonente.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PonentesSerializer
