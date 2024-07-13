from django.db import models
from Bloque.models import MaeBloque
from CongresoJINIS.models import MaeCongresoJinis

# Create your models here.
class MaeColaborador(models.Model):
    idcolaborador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=30)
    correo = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=8)
    idtipo = models.ForeignKey('MaeTipousuario', models.DO_NOTHING, db_column='idtipo')
    idbloque = models.ForeignKey(MaeBloque, models.DO_NOTHING, db_column='idbloque')
    idcongreso = models.ForeignKey(MaeCongresoJinis, models.DO_NOTHING, db_column='idcongreso')
    
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