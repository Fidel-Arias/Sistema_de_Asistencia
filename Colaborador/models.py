from django.db import models
from Bloque.models import MaeBloque
from tipoUsuario.models import MaeTipoUsuario

# Create your models here.
class MaeColaborador(models.Model):
    idcolaborador = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=40, null=False)
    apellidos = models.CharField(max_length=40, null=False)
    correo = models.CharField(max_length=40, null=False)
    contrasenia = models.CharField(null=False)
    idtipo = models.ForeignKey(MaeTipoUsuario, db_column='idtipo', on_delete=models.CASCADE, null=False)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)
    
    class Meta:
        managed = False
        db_table = 'mae_colaborador'

    def __str__(self) -> str:
        return self.nombres + ' ' + self.apellidos