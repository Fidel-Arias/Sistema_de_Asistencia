from django.db import models
from Ponente.models import MaePonente
from Congreso.models import MaeCongreso

# Create your models here.
class MaePonencia(models.Model):
    idponencia = models.AutoField(primary_key=True)
    idponente = models.ForeignKey(MaePonente, db_column='idponente', on_delete=models.CASCADE, null=False)
    nombre = models.CharField(max_length=50, blank=False, null=False)
    idcongreso = models.ForeignKey(MaeCongreso, db_column='idcongreso', null=False, on_delete=models.CASCADE)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)

    class Meta:
        managed = False 
        db_table = 'mae_ponencia'

    def __str__(self):
        return f'{self.nombre}'