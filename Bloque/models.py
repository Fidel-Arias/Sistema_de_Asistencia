from django.db import models
from Dia.models import MaeDia
from Ponencia.models import MaePonencia
from Ubicacion.models import MaeUbicacion
from CongresoJINIS.models import MaeCongresoJinis

# Create your models here.
class MaeBloque(models.Model):
    idbloque = models.AutoField(primary_key=True)
    idponencia = models.ForeignKey(MaePonencia, db_column='idponencia', verbose_name='Ponencia', on_delete=models.CASCADE)
    iddia = models.ForeignKey(MaeDia, db_column='iddia', verbose_name='Dia', on_delete=models.CASCADE)
    horainicio = models.TimeField(verbose_name='Desde')
    horafin = models.TimeField(verbose_name='Hasta')
    idubicacion = models.ForeignKey(MaeUbicacion, db_column='idubicacion', on_delete=models.CASCADE)
    idcongreso = models.ForeignKey(MaeCongresoJinis, db_column='idcongreso', null=False, on_delete=models.CASCADE)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)

    class Meta:
        managed = False
        db_table = 'mae_bloque'

    def __str__(self):
        return f'{self.iddia} : {(self.horainicio.strftime("%H:%M %p")).lower()} - {(self.horafin.strftime("%H:%M %p")).lower()}'

