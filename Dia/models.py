from django.db import models
from CongresoJINIS.models import MaeCongresoJinis

# Create your models here.
class MaeDia(models.Model):
    iddia = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=False, null=False)
    estado = models.CharField(max_length=11, default='ACTIVO')
    idcongreso = models.ForeignKey(MaeCongresoJinis, null=False, db_column='idcongreso', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mae_dia'

    def __str__(self):
        return f'{self.fecha.day} de { meses(self.fecha.month) }'

def meses(fecha):
    if fecha == 1:
        return 'Enero'
    elif fecha == 2:
        return 'Febrero'
    elif fecha == 3:
        return 'Marzo'
    elif fecha == 4:
        return 'Abril'
    elif fecha == 5:
        return 'Mayo'
    elif fecha == 6:
        return 'Junio'
    elif fecha == 7:
        return 'Julio'
    elif fecha == 8:
        return 'Agosto'
    elif fecha == 9:
        return 'Septiembre'
    elif fecha == 10:
        return 'Octubre'
    elif fecha == 11:
        return 'Noviembre'
    elif fecha == 12:
        return 'Diciembre'
