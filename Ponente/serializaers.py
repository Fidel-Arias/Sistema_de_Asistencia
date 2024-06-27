from rest_framework import serializers
from .models import MaePonente

class PonentesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaePonente
        fields = ('idponente', 'nombre', 'apellido')