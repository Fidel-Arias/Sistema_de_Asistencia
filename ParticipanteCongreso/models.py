from django.db import models
from Participantes.models import MaeParticipantes
from Congreso.models import MaeCongreso


# Create your models here.
class ParticipanteCongreso(models.Model):
    idpc = models.AutoField(primary_key=True)
    codparticipante = models.ForeignKey(MaeParticipantes, max_length=20, null=False, db_column='codparticipante', on_delete=models.CASCADE)
    idcongreso = models.ForeignKey(MaeCongreso, db_column='idcongreso', null=False, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'participante_congreso'
    
    
