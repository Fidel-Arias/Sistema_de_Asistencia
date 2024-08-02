from django.db import models
from tipoUsuario.models import MaeTipoUsuario
from Congreso.models import MaeCongreso


class MaeAdministrador(models.Model):
    idadministrador = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=40, null=False)
    apellidos = models.CharField(max_length=40, null=False)
    correo = models.CharField(max_length=50, null=False)
    contrasenia = models.CharField(null=False)
    idtipo = models.ForeignKey(MaeTipoUsuario, db_column='idtipo', on_delete=models.CASCADE, null=False)
    idcongreso = models.ForeignKey(MaeCongreso, db_column='idcongreso', null=False, on_delete=models.CASCADE)
    estado = models.CharField(max_length=11, default='ACTIVO')

    class Meta:
        managed = False
        db_table = 'mae_administrador'

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'