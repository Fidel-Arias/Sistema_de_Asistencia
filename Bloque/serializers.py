from rest_framework import serializers
from .models import MaeBloque

class BloqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaeBloque
        fields = ('idbloque', 'idponencia', 'iddia', 'horainicio', 'horafin', 'direccion')