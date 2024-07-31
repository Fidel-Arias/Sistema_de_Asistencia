from django.db import models
from Ponente.models import MaePonente
from CongresoJINIS.models import MaeCongresoJinis

# Create your models here.
class MaePonencia(models.Model):
    idponencia = models.AutoField(primary_key=True)
    idponente = models.ForeignKey(MaePonente, db_column='idponente', verbose_name='Ponente', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=40, blank=False, null=False)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)
    idcongreso = models.ForeignKey(MaeCongresoJinis, db_column='idcongreso', null=False, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mae_ponencia'

    def __str__(self):
        return f'{self.nombre}'