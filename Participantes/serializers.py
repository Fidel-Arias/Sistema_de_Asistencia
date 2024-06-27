from rest_framework import serializers
from .models import MaeParticipantes

class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaeParticipantes
        fields = ('codparticipante', 'nombre', 'apellido', 'email', 'idtipodoc', 'iduniversidad', 'idtipo')
        read_only_fields = ('codparticipante', 'nombre', 'apellido', 'email', 'idtipodoc','iduniversidad', 'idtipo')
