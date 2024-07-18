from django.db import models
from tipoDocumento.models import MaeTipodocumento
from Universidad.models import MaeUniversidad
from tipoParticipante.models import MaeTipoParticipante


class MaeParticipantes(models.Model):
    codparticipante = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=20)
    email = models.CharField(max_length=35)
    idtipodoc = models.ForeignKey(MaeTipodocumento, models.DO_NOTHING, db_column='idtipodoc')
    iduniversidad = models.ForeignKey(MaeUniversidad, models.DO_NOTHING, db_column='iduniversidad')
    idtipo = models.ForeignKey(MaeTipoParticipante, models.DO_NOTHING, db_column='idtipo')
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)

    class Meta:
        managed = False
        db_table = 'mae_participantes'

    def __str__(self) -> str:
        return self.codparticipante


















