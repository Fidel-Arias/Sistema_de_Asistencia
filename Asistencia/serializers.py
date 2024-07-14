from rest_framework import serializers
from .models import TrsAsistencia
from Ponencia.serializers import PonenciasSerializer
from CongresoJINIS.serializers import CongresoJinisSerializer
from Participantes.serializers import ParticipanteSerializer
from Bloque.serializers import BloqueSerializer
from Dia.serializers import DiaSerializer
from Universidad.serializers import UniversidadSerializer
from Dia.models import MaeDia


class AsistenciaSerializer(serializers.ModelSerializer):
    codparticipante = ParticipanteSerializer()
    idcongreso = CongresoJinisSerializer()
    idbloque = BloqueSerializer()
    idponencia = PonenciasSerializer(source='idbloque.idponencia')
    iddia = DiaSerializer(source='idbloque.iddia')
    iduniversidad = UniversidadSerializer(source='codparticipante.iduniversidad')

    class Meta:
        model = TrsAsistencia
        fields = ('idcongreso', 'codparticipante', 'iddia', 'iduniversidad', 'idponencia','idbloque', 'fecha', 'hora', 'estado')
        read_only_fields = ('fecha', 'hora', 'estado')