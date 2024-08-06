from django.db import models
from Dia.models import MaeDia
from Ponencia.models import MaePonencia
from Ubicacion.models import MaeUbicacion

# Create your models here.
class MaeBloque(models.Model):
    idbloque = models.AutoField(primary_key=True)
    idponencia = models.ForeignKey(MaePonencia, db_column='idponencia', null=False, on_delete=models.CASCADE)
    iddia = models.ForeignKey(MaeDia, db_column='iddia', null=False, on_delete=models.CASCADE)
    horainicio = models.TimeField(verbose_name='Desde', null=False)
    horafin = models.TimeField(verbose_name='Hasta', null=False)
    idubicacion = models.ForeignKey(MaeUbicacion, db_column='idubicacion', on_delete=models.CASCADE, null=False)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)

    class Meta:
        managed = False
        db_table = 'mae_bloque'

    def __str__(self):
        return f'{(self.horainicio.strftime("%H:%M %p")).lower()} - {(self.horafin.strftime("%H:%M %p")).lower()} : {self.idponencia}'

