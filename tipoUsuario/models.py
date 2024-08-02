from django.db import models

# Create your models here.
class MaeTipoUsuario(models.Model):
    idtipo = models.AutoField(primary_key=True)
    dstipo = models.CharField(max_length=30, blank=False, null=False)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)

    class Meta:
        managed = False
        db_table = 'mae_tipousuario'
    
    def __str__(self):
        return self.dstipo