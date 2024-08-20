from .models import MaeCongreso

def creando_nuevo_congreso(formulario):
    #Validar q no se repia congreso y agregar la tabla admin congreso y quitar las opcones select
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
    except Exception:
        return 'failed'

    