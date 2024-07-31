from django.db import models
from CongresoJINIS.models import MaeCongresoJinis

# Create your models here.
class MaePonente(models.Model):
    idponente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10, blank=True, null=True)
    apellido = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)
    idcongreso = models.ForeignKey(MaeCongresoJinis, db_column='idcongreso', null=False, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mae_ponente'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'