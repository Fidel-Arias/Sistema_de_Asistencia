from rest_framework import viewsets, permissions
from rest_framework import serializers
from .models import TrsAsistencia

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrsAsistencia
        fields = '__all__'
        read_only_fields = ('fecha', 'hora', 'estado')
