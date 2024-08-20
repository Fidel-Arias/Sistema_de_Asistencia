from django.db import connection
from django.shortcuts import render, redirect
from ..decorators import administrador_login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from Bloque.models import MaeBloque
from Bloque.forms import BloqueForm
from Ponencia.models import MaePonencia
from Dia.models import MaeDia
from Congreso.models import MaeCongreso
from Ubicacion.models import MaeUbicacion
from django.contrib import messages

class Registrar_Bloques(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def registrar_bloques(self, request, pk):
        if request.method == 'POST':
            ponencia = request.POST.get('ponencia')
            dia = request.POST.get('dia')
            horaInicio = request.POST.get('hora_inicio')
            horaFin = request.POST.get('hora_fin')
            ubicacion = request.POST.get('ubicacion')
            action = request.POST.get('action')
            idcongreso = request.POST.get('congreso')

            if idcongreso:
                selected_congreso = idcongreso
            else:
                selected_congreso = None
            
            if action == 'register':
                if not MaeBloque.objects.filter(idponencia=ponencia).exists():
                    try:
                        if horaInicio == horaFin:
                            messages.error(request, "La hora inicial y final deben ser diferentes")
                        elif horaFin < horaInicio:
                            messages.error(request, "La hora inicial no puede ser mayor a la hora final")
                        else:
                            resultado = verificar_ubicacion(0, ponencia, horaInicio, horaFin, ubicacion)
                            if resultado == 'OK':
                                nuevo_bloque = MaeBloque(
                                    idponencia=MaePonencia.objects.get(pk=ponencia),
                                    iddia= MaeDia.objects.get(pk=dia),
                                    horainicio=horaInicio,
                                    horafin=horaFin,
                                    idubicacion=MaeUbicacion.objects.get(pk=ubicacion)
                                )
                                nuevo_bloque.save()
                                messages.success(request, "El bloque ha sido creado exitosamente")
                            else:
                                messages.error(request, "El auditorio no esta disponible para la hora indicada")
                    except Exception:
                        messages.error(request, 'Se produjo un error al crear el bloque')
                else:
                    messages.error(request, "Ya existe una ponencia en los bloques")
                return redirect(reverse('RegistrarBloques', kwargs={'pk':pk}))
            elif action == 'delete':
                try:
                    bloque = MaeBloque.objects.get(idponencia=ponencia, iddia=dia, horainicio=horaInicio, horafin=horaFin, idubicacion=ubicacion)
                    #ELIMINACION TOTAL
                    '''bloque.delete()'''
                    #ELIMINACION LOGICA
                    bloque.estado = "NO ACTIVO"
                    bloque.save()
                    messages.success(request, 'El bloque ha sido desactivado exitosamente')
                except MaeBloque.DoesNotExist:
                    messages.error(request, 'El bloque no existe')
                except Exception:
                    messages.error(request, 'Se produjo un error al desactivar el bloque')
                return redirect(reverse('RegistrarBloques', kwargs={'pk':pk}))
            elif action == 'activate':
                try:
                    bloque = MaeBloque.objects.get(idponencia=ponencia, iddia=dia, horainicio=horaInicio, horafin=horaFin, idubicacion=ubicacion)
                    bloque.estado = "ACTIVO"
                    bloque.save()
                    messages.success(request, 'El bloque ha sido activado exitosamente')
                except MaeBloque.DoesNotExist:
                    messages.error(request, 'El bloque no existe')
                except Exception:
                    messages.error(request, 'Se produjo un error al activar el bloque')
                return redirect(reverse('RegistrarBloques', kwargs={'pk':pk}))
            elif action == 'edit':
                idbloque = request.POST.get('id');
                try:
                    bloque = MaeBloque.objects.get(pk=idbloque)
                    contexto = {
                        'idponencia': ponencia,
                        'iddia': dia,
                        'horainicio': horaInicio,
                        'horafin': horaFin,
                        'idubicacion': ubicacion
                    }
                    bloque_actualizado = BloqueForm(contexto, instance=bloque)
                    if bloque_actualizado.is_valid():
                        bloque_actualizado.save()
                        messages.success(request, 'El bloque ha sido actualizado exitosamente')
                    else:
                        messages.error(request, 'Se produjo un error al actualizar el bloque')
                except MaeBloque.DoesNotExist:
                    messages.error(request, 'El bloque no existe')
                except Exception:
                    messages.error(request, 'Se produjo un error al actualizar el bloque')
                return redirect(reverse('RegistrarBloques', kwargs={'pk':pk}))
            
            if not MaePonencia.objects.filter(idcongreso=idcongreso).exists() or not MaePonencia.objects.filter(estado='ACTIVO').exists():
                messages.warning(request,'No hay ponencias registradas o activas, por favor registre al menos una')
            elif not MaeDia.objects.filter(idcongreso=idcongreso).exists() or not MaeDia.objects.filter(estado='ACTIVO').exists():
                messages.warning(request, 'No hay días registrados o activos, por favor registre al menos un día')
            elif not MaeUbicacion.objects.filter(estado='ACTIVO').exists() or not MaeUbicacion.objects.filter().exists():
                messages.warning(request, 'No hay ubicaciones registradas o activas, por favor registre al menos una ubicación')
            bloques = MaeBloque.objects.all().order_by('pk')
            lista_ponencias = MaePonencia.objects.filter(idcongreso=idcongreso, estado='ACTIVO').order_by('pk')
            lista_dias = MaeDia.objects.filter(idcongreso=idcongreso, estado='ACTIVO').order_by('pk')
            ubicaciones = MaeUbicacion.objects.filter(estado='ACTIVO').order_by('pk')
            congresos = MaeCongreso.objects.filter(estado="ACTIVO").order_by('pk')
            return render(request, 'pages/registrarBloques.html', {
                'current_page': 'registrar_bloques', 
                'ponencias': lista_ponencias, 
                'dias': lista_dias, 
                'ubicaciones':ubicaciones, 
                'bloques':bloques, 
                'selected_congreso':int(selected_congreso), 
                'congresos':congresos,
                'pk': pk
            })
        else:
            bloques = MaeBloque.objects.filter().order_by('pk')
            congresos = MaeCongreso.objects.all().order_by('pk')
            if not MaeCongreso.objects.filter().exists() or not MaeCongreso.objects.filter(estado='ACTIVO').exists():
                messages.warning(request, 'No hay congresos registrados, por favor registre al menos un congreso')
            return render(request, 'pages/registrarBloques.html', {
                'current_page': 'registrar_bloques', 
                'bloques':bloques, 
                'selected_congreso':None, 
                'congresos':congresos,
                'pk': pk
            })
    

def verificar_ubicacion(id, fecha, hora_inicio, hora_fin, ubicacion):
    cursor = connection.cursor()
    cursor.callproc('verificar_ubicacion', [id, fecha, hora_inicio, hora_fin, ubicacion])
    resultado = cursor.fetchone()[0]
    return resultado