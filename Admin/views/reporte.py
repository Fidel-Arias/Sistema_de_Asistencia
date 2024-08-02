from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Asistencia.models import TrsAsistencia
# from Asistencia.serializers import AsistenciaSerializer
from Congreso.models import MaeCongreso

@login_required
def generar_reporte(request):
    asistenciaObjetcs = TrsAsistencia.objects.all().order_by('pk')
    listaAsistencia = TrsAsistencia.objects.all().order_by('pk')
    congresos = MaeCongreso.objects.all().order_by('pk')
    return render(request, 'pages/generarReporte.html', {
        'current_page':'generar_reportes', 
        'listaAsistencia': listaAsistencia, 
        'congresos':congresos
    })