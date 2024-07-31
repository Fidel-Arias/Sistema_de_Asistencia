from django.db import models
from tipoDocumento.models import MaeTipodocumento
from CongresoJINIS.models import MaeCongresoJinis


class MaeParticipantes(models.Model):
    codparticipante = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=40, null=False)
    ap_paterno = models.CharField(max_length=40, null=False)
    ap_materno = models.CharField(max_length=40, null=False)
    correo = models.CharField(max_length=40, null=False)
    idtipodoc = models.ForeignKey(MaeTipodocumento, db_column='idtipodoc', on_delete=models.CASCADE, null=False)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)
    idcongreso = models.ForeignKey(MaeCongresoJinis, null=False, db_column='idcongreso', on_delete=models.CASCADE)
    qr_code = models.CharField(max_length=255, null=True)

    class Meta:
        managed = False
        db_table = 'mae_participantes'

    def __str__(self) -> str:
        return self.nombre + self.ap_paterno + self.ap_materno


















