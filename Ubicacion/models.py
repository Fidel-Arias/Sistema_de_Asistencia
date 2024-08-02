from django.db import models

# Create your models here.
class MaeUbicacion(models.Model):
    idubicacion = models.AutoField(primary_key=True)
    ubicacion = models.CharField(max_length=60, null=False)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)

    def __str__(self) -> str:
        return self.ubicacion

    class Meta:
        managed = False
        db_table = 'mae_ubicacion'