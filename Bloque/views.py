from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import MaeBloque
from .serializers import BloqueSerializer

# Create your views here.
class viewBloques(viewsets.ModelViewSet):
    queryset = MaeBloque.objects.all()
    #permission_classes = [permissions.AllowAny] #permisos admin
    serializer_class = BloqueSerializer