from rest_framework import serializers
from .models import MaeAdministrador

class AdminSerializer(serializers.Serializer):
    class Meta:
        model = MaeAdministrador
        fields = ('idadministrador', 'nombre', 'apellido', 'correo', 'contrasenia')
        read_only_fields = ('idadministrador', 'nombre', 'apellido')