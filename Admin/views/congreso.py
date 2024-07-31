from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from CongresoJINIS.models import MaeCongresoJinis
from CongresoJINIS.forms import CongresoJinisForm
from Dia.models import MaeDia
from django.contrib import messages
from datetime import date
import pandas as pd

@login_required
def registrar_congreso(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        nombreCongreso = request.POST.get('nombreCongreso')
        fechaHoy = date.today()
        fechaInicio = request.POST.get('fechaInicio')
        fechaFin = request.POST.get('fechaFin')
        asistenciaTotal = request.POST.get('totalAsistencia')
        if action == 'register':
            if fechaInicio == fechaFin:
                messages.error(request, 'Las fechas de inicio y fin deben ser distintas')
            elif fechaFin < fechaInicio:
                messages.error(request, 'Ingrese correctamente las fechas')
            elif fechaInicio < fechaHoy.__str__() or fechaFin < fechaHoy.__str__():
                messages.error(request, 'La fecha de inicio y fin no puede ser anterior a la fecha de hoy')
            else:
                try:
                    if (not(MaeCongresoJinis.objects.filter(nombre=nombreCongreso).exists()) and not(MaeCongresoJinis.objects.filter(fechainicio=fechaInicio, fechafin=fechaFin).exists())):
                        nueva_congreso = MaeCongresoJinis(
                            nombre=nombreCongreso,
                            fechainicio=fechaInicio,
                            fechafin=fechaFin,
                            asistenciatotal=asistenciaTotal
                        )
                        nueva_congreso.save()
                        congreso = MaeCongresoJinis.objects.get(nombre=nombreCongreso)
                        generacion_ingreso_tabla_dias(request, fechaInicio, fechaFin, congreso.idcongreso)
                        messages.success(request, 'Congreso registrado con éxito')
                    else:
                        messages.error(request, 'Ya existe el congreso')
                        print('bien el mensaje')
                except Exception:
                    messages.error(request, 'Error al registrar el congreso')
            return redirect('RegistrarCongreso')
        elif action == 'delete':
            try:
                congreso = MaeCongresoJinis.objects.get(nombre=nombreCongreso)
                #ELIMINACION TOTAL
                '''congreso.delete()'''
                #ELIMINACION LOGICA
                congreso.estado = 'NO ACTIVO'
                congreso.save()
                desactivarDias(request, congreso.idcongreso)
                messages.success(request, 'Congreso desactivado con éxito')
            except MaeCongresoJinis.DoesNotExist:
                messages.error(request, 'No se encontró el congreso')
            except Exception as e:
                messages.error(request, e)
            return redirect('RegistrarCongreso')
        elif action == 'activate':
            try:
                congreso = MaeCongresoJinis.objects.get(nombre=nombreCongreso)
                congreso.estado = 'ACTIVO'
                congreso.save()
                activarDias(request, congreso.idcongreso)
                messages.success(request, 'Congreso activado con éxito')
            except MaeCongresoJinis.DoesNotExist:
                messages.error(request, 'No se encontró el congreso')
            except Exception:
                messages.error(request, 'Error al activar el congreso')
            return redirect('RegistrarCongreso')
        elif action == 'edit':
            idcongreso = request.POST.get('id')
            print('id congreso: ', idcongreso)
            if fechaInicio == fechaFin:
                messages.error(request, 'Las fechas de inicio y fin deben ser distintas')
            elif fechaFin < fechaInicio:
                messages.error(request, 'Ingrese correctamente las fechas')
            elif fechaInicio < fechaHoy.__str__() or fechaFin < fechaHoy.__str__():
                messages.error(request, 'La fecha de inicio y fin no puede ser anterior a la fecha de hoy')
            try:
                congreso = MaeCongresoJinis.objects.get(pk=idcongreso)
                contexto = {
                    'nombre': nombreCongreso,
                    'fechainicio': fechaInicio,
                    'fechafin': fechaFin,
                    'asistenciatotal': asistenciaTotal,
                }
                congreso_actualizado = CongresoJinisForm(contexto, instance=congreso)
                if congreso_actualizado.is_valid():
                    congreso_actualizado.save()
                    editarDias(request, idcongreso, fechaInicio, fechaFin)
                    messages.success(request, 'Congreso actualizado con éxito')
                else:
                    messages.error(request, congreso_actualizado.errors)
            except MaeCongresoJinis.DoesNotExist:
                messages.error(request, 'El congreso ya no existe')
            return redirect('RegistrarCongreso')
    else:
        congresos = MaeCongresoJinis.objects.all().order_by('pk')
        return render(request, 'pages/registrarCongreso.html', {'current_page': 'registrar_congreso', 'congresos':congresos})
    

def generacion_ingreso_tabla_dias(request, fechaInicio, fechaFin, idcongreso):
    try:
        date_range = pd.date_range(start=fechaInicio, end=fechaFin) #Generación de rangos desde la fecha de inicio hasta la fecha fin
        date_list = date_range.strftime('%Y-%m-%d').tolist()
        lista_dias = None
        for i in range(0, len(date_list)):
            lista_dias = MaeDia(
                fecha = date_list[i],
                idcongreso = MaeCongresoJinis.objects.get(pk=idcongreso)
            )
            lista_dias.save()
        messages.success(request, 'Se generaron los dias del congreso con éxito')
    except Exception:
        messages.error(request, 'Error al generar los dias del congreso')
        return redirect('RegistrarCongreso')

def desactivarDias(request, idcongreso):
    try:
        dias = MaeDia.objects.filter(idcongreso=idcongreso)
        for i in range(0, len(dias)):
            dias[i].estado = 'NO ACTIVO'
            dias[i].save()
        messages.success(request, 'Dias del congreso desactivados con éxito')
    except MaeDia.DoesNotExist:
        messages.error(request, 'No se encontró el día del congreso')
    except Exception:
        messages.error(request, 'Error al desactivar los dias del congreso')
    return redirect('RegistrarCongreso')

def activarDias(request, idcongreso):
    try:
        dias = MaeDia.objects.filter(idcongreso=idcongreso)
        for i in range(0, len(dias)):
            dias[i].estado = 'ACTIVO'
            dias[i].save()
        messages.success(request, 'Dias del congreso activados con éxito')
    except MaeDia.DoesNotExist:
        messages.error(request, 'No se encontró el día del congreso')
    except Exception:
        messages.error(request, 'Error al activar los dias del congreso')
    return redirect('RegistrarCongreso')

def editarDias(request, idcongreso, fechaInicio, fechaFin):
    try:
        date_range = pd.date_range(start=fechaInicio, end=fechaFin) #Generación de rangos desde la fecha de inicio hasta la fecha fin
        date_list = date_range.strftime('%Y-%m-%d').tolist()
        dias = MaeDia.objects.filter(idcongreso=idcongreso).order_by('pk')
        dias.delete()
        for i in range(0, len(date_list)):
            lista_dias = MaeDia(
                fecha = date_list[i],
                idcongreso = MaeCongresoJinis.objects.get(pk=idcongreso)
            )
            lista_dias.save()
        messages.success(request, 'Se editaron los dias del congreso con éxito')
    except MaeDia.DoesNotExist:
        messages.error(request, 'No se encontró el día del congreso')
    except Exception as e:
        messages.error(request, e)
    return redirect('RegistrarCongreso')