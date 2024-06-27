from django.db import models

# Create your models here.
class MaeUniversidad(models.Model):
    iduniversidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    ruc = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'mae_universidad'

    def __str__(self):
        return self.nombre