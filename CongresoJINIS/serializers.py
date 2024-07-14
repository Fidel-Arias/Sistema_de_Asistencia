from rest_framework import serializers
from .models import MaeCongresoJinis

class CongresoJinisSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaeCongresoJinis
        fields = ('idcongreso', 'nombre', 'fechainicio', 'fechafin')