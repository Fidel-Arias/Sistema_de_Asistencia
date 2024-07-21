from django.db import models

# Create your models here.
class MaeCongresoJinis(models.Model):
    idcongreso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    fechainicio = models.DateField(blank=False, null=False)
    fechafin = models.DateField(blank=False, null=False)
    asistenciatotal = models.IntegerField(blank=False, null=False)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)

    class Meta:
        managed = False
        db_table = 'mae_congreso_jinis'

    def __str__(self) -> str:
        return self.nombre