from rest_framework import viewsets, permissions
from rest_framework import serializers
from .models import TrsAsistencia

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrsAsistencia
        fields = ('idcongreso','codparticipante','idbloque','fecha','hora','estado')
        read_only_fields = ('fecha', 'hora', 'estado')
