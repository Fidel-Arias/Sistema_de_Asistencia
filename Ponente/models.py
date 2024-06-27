from django.db import models

# Create your models here.
class MaePonente(models.Model):
    idponente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10, blank=True, null=True)
    apellido = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mae_ponente'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'