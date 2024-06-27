from rest_framework import serializers
from .models import MaeUniversidad

class UniversidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaeUniversidad
        fields = ('iduniversidad', 'nombre', 'ruc')