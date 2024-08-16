from .models import MaeCongreso

def creando_nuevo_congreso(formulario):
    try:
        nombre = formulario['nombreCongreso']
        asistencias = formulario['asistencia']
        fecha_inicio = formulario['fechaInicioCongreso']
        fecha_fin = formulario['fechaFinCongreso']

        nuevo_congreso = MaeCongreso(
            nombre=nombre,
            asistenciatotal=asistencias,
            fechainicio=fecha_inicio,
            fechafin=fecha_fin
        )

        nuevo_congreso.save()
        return 'success'
    except MaeCongreso.DoesNotExist:
        return 'failed'

    