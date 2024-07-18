from django.db import models
from Bloque.models import MaeBloque
from CongresoJINIS.models import MaeCongresoJinis
from tipoUsuario.models import MaeTipoUsuario

# Create your models here.
class MaeColaborador(models.Model):
    idcolaborador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=30)
    correo = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=8)
    idtipo = models.ForeignKey('MaeTipousuario', models.DO_NOTHING, db_column='idtipo')
    idcongreso = models.ForeignKey('MaeCongresoJinis', models.DO_NOTHING, db_column='idcongreso')
    estado = models.CharField(max_length=11)
    
    class Meta:
        managed = False
        db_table = 'mae_colaborador'

    def __str__(self) -> str:
        return self.nombre