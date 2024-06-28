from django.db import models
from Asistencia.models import TrsAsistencia

# Create your models here.
class MaeColaborador(models.Model):
    idcolaborador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=30)
    correo = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=8)
    idtipo = models.ForeignKey('MaeTipousuario', models.DO_NOTHING, db_column='idtipo')
    
    class Meta:
        managed = False
        db_table = 'mae_colaborador'

    def __str__(self) -> str:
        return self.nombre

class MaeTipousuario(models.Model):
    idtipo = models.AutoField(primary_key=True)
    dstipo = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'mae_tipousuario'