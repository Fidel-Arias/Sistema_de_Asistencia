
from django.db import models

class BloqueColaborador(models.Model):
    idbc = models.AutoField(primary_key=True)
    idcolaborador = models.ForeignKey('MaeColaborador', models.DO_NOTHING, db_column='idcolaborador')
    idbloque = models.ForeignKey('MaeBloque', models.DO_NOTHING, db_column='idbloque')

    class Meta:
        managed = False
        db_table = 'bloque_colaborador'











