from django.shortcuts import render
from rest_framework import viewsets
from .models import MaePonente
from .serializaers import PonentesSerializer

# Create your views here.
class viewPonentes(viewsets.ModelViewSet):
    queryset = MaePonente.objects.all()
    serializer_class = PonentesSerializer
