from django.db import models
from Dia.models import MaeDia
from Ponencia.models import MaePonencia

# Create your models here.
class MaeBloque(models.Model):
    idbloque = models.AutoField(primary_key=True)
    idponencia = models.ForeignKey(MaePonencia, models.DO_NOTHING, db_column='idponencia', verbose_name='Ponencia')
    iddia = models.ForeignKey(MaeDia, models.DO_NOTHING, db_column='iddia', verbose_name='Dia')
    horainicio = models.TimeField(verbose_name='Desde')
    horafin = models.TimeField(verbose_name='Hasta')
    direccion = models.CharField(blank=False, null=False, max_length=40)

    class Meta:
        managed = False
        db_table = 'mae_bloque'

    def __str__(self):
        return f'{self.iddia} : {self.horainicio.strftime("%H:%M %p")} - {self.horafin.strftime("%H:%M %p")}'

