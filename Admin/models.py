from django.db import models

class MaeAdministrador(models.Model):
    idadministrador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=30)
    correo = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=20)
    idtipo = models.ForeignKey('MaeTipousuario', models.DO_NOTHING, db_column='idtipo')
    estado = models.CharField(max_length=11, default='ACTIVO')

    class Meta:
        managed = False
        db_table = 'mae_administrador'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'