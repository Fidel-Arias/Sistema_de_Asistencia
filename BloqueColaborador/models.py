from Colaborador.models import MaeColaborador
from Bloque.models import MaeBloque
from django.db import models

class BloqueColaborador(models.Model):
    idbc = models.AutoField(primary_key=True)
    idcolaborador = models.ForeignKey(MaeColaborador, db_column='idcolaborador', on_delete=models.CASCADE)
    idbloque = models.ForeignKey(MaeBloque, db_column='idbloque', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'bloque_colaborador'











