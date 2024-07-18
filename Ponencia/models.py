from django.db import models
from Ponente.models import MaePonente

# Create your models here.
class MaePonencia(models.Model):
    idponencia = models.AutoField(primary_key=True)
    idponente = models.ForeignKey(MaePonente, models.DO_NOTHING, db_column='idponente', verbose_name='Ponente')
    nombre = models.CharField(max_length=40, blank=False, null=False)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)

    class Meta:
        managed = False
        db_table = 'mae_ponencia'

    def __str__(self):
        return f'{self.nombre}'