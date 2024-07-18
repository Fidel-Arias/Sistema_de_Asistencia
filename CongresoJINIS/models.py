from django.db import models

# Create your models here.
class MaeCongresoJinis(models.Model):
    idcongreso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    fechainicio = models.DateField()
    fechafin = models.DateField()
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)

    class Meta:
        managed = False
        db_table = 'mae_congreso_jinis'

    def __str__(self) -> str:
        return self.nombre