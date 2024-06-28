from rest_framework import serializers
from .models import MaeColaborador

class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaeColaborador
        fields = ('idcolaborador', 'nombre', 'apellido', 'correo', 'contrasenia', 'idtipo')
        read_only_fields = ('idcolaborador')