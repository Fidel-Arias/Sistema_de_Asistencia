from django.db import models

# Create your models here.
class MaeTipoParticipante(models.Model):
    idtipo = models.AutoField(primary_key=True)
    dstipo = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self) -> str:
        return self.dstipo

    class Meta:
        managed = False
        db_table = 'mae_tipo_participante'