from Colaborador.models import MaeColaborador
from Bloque.models import MaeBloque
from django.db import models
from Congreso.models import MaeCongreso

class BloqueColaborador(models.Model):
    idbc = models.AutoField(primary_key=True)
    idcolaborador = models.ForeignKey(MaeColaborador, db_column='idcolaborador', on_delete=models.CASCADE, null=False)
    idbloque = models.ForeignKey(MaeBloque, db_column='idbloque', on_delete=models.CASCADE, null=False)
    idcongreso = models.ForeignKey(MaeCongreso, db_column='idcongreso', null=False, on_delete=models.CASCADE)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)

    class Meta:
        managed = False
        db_table = 'bloque_colaborador'











