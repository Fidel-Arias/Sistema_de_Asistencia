from django.db import models
from CongresoJINIS.models import MaeCongresoJinis
from Participantes.models import MaeParticipantes
from Bloque.models import MaeBloque
from BloqueColaborador.models import BloqueColaborador
from rest_framework.decorators import action

# Create your models here.
class TrsAsistencia(models.Model):
    idasistencia = models.AutoField(primary_key=True)
    idcongreso = models.ForeignKey(MaeCongresoJinis, models.DO_NOTHING, db_column='idcongreso', blank=False, verbose_name='Congreso')
    codparticipante = models.ForeignKey(MaeParticipantes, models.DO_NOTHING, db_column='codparticipante', verbose_name='DNI o Carnet')
    idbc = models.ForeignKey(BloqueColaborador, models.DO_NOTHING, db_column='idbc')
    fecha = models.DateField(auto_now_add=True, blank=False, null=False)
    hora = models.TimeField(auto_now_add=True, blank=False, null=False)
    estado = models.CharField(max_length=11, default='ACTIVO', null=False)

    class Meta:
        managed = False
        db_table = 'trs_asistencia'


    