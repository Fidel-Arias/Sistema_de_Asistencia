from django.db import models
from tipoDocumento.models import MaeTipodocumento
from tipoParticipante.models import MaeTipoParticipante


class MaeParticipantes(models.Model):
    codparticipante = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(null=False)
    ap_paterno = models.CharField(null=False)
    ap_materno = models.CharField(null=False)
    correo = models.CharField(null=False)
    idtipodoc = models.ForeignKey(MaeTipodocumento, db_column='idtipodoc', on_delete=models.CASCADE, null=False)
    idtipo = models.ForeignKey(MaeTipoParticipante, db_column='idtipo', on_delete=models.CASCADE, null=False)
    qr_code = models.CharField(null=True)

    class Meta:
        managed = False
        db_table = 'mae_participantes'

    def __str__(self) -> str:
        return self.nombre + self.ap_paterno + self.ap_materno


















