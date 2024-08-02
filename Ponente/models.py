from django.db import models

# Create your models here.
class MaePonente(models.Model):
    idponente = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=40, blank=True, null=False)
    apellidos = models.CharField(max_length=40, blank=True, null=False)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)

    class Meta:
        managed = False
        db_table = 'mae_ponente'

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'