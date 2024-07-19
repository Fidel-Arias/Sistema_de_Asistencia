from django.db import models
from tipoUsuario.models import MaeTipoUsuario

class MaeAdministrador(models.Model):
    idadministrador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=30)
    correo = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=20)
    idtipo = models.ForeignKey(MaeTipoUsuario, db_column='idtipo', on_delete=models.CASCADE)
    estado = models.CharField(max_length=11, default='ACTIVO')

    class Meta:
        managed = False
        db_table = 'mae_administrador'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'