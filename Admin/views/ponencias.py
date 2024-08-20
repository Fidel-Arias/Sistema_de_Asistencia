from django.shortcuts import render, redirect
from django.urls import reverse
from ..decorators import administrador_login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from Ponencia.models import MaePonencia
from Ponencia.forms import PonenciaForm
from Ponente.models import MaePonente
from Congreso.models import MaeCongreso
from django.contrib import messages

class Registrar_Ponencias(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def registrar_ponencias(self, request, pk):
        if request.method == 'POST':
            action = request.POST.get('action')
            ponente = request.POST.get('ponente')
            nombrePonencia = request.POST.get('nombre_ponencia')
            idcongreso = request.POST.get('congreso')

            if idcongreso:
                selected_congreso = idcongreso
            else:
                selected_congreso = None

            if action == 'register':
                try:
                    if (not(MaePonencia.objects.filter(nombre=nombrePonencia).exists())):
                        nueva_ponencia = MaePonencia(
                            nombre=nombrePonencia,
                            idponente=MaePonente.objects.get(pk=ponente),
                            idcongreso=MaeCongreso.objects.get(pk=idcongreso)
                        )
                        nueva_ponencia.save()
                        messages.success(request, 'Ponencia registrada con éxito')
                    else:
                        messages.error(request, 'Ya existe la ponencia')
                except Exception:
                    messages.error(request, 'Error al registrar la ponencia')
                return redirect(reverse('RegistrarPonencia', kwargs={'pk':pk}))
            elif action == 'delete':
                try:
                    ponencia = MaePonencia.objects.get(nombre=nombrePonencia)
                    #ELIMINACION TOTAL
                    '''ponencia.delete()'''
                    #ELIMINACION LOGICA
                    ponencia.estado = 'NO ACTIVO'
                    ponencia.save()
                    messages.success(request, 'Ponencia desactivada con éxito')
                except MaePonencia.DoesNotExist:
                    messages.error(request, 'No se encontró la ponencia')
                except Exception:
                    messages.error(request, 'Error al desactivar la ponencia')
                return redirect(reverse('RegistrarPonencia', kwargs={'pk':pk}))
            elif action == 'activate':
                idponencia = request.POST.get('id')
                try:
                    ponencia = MaePonencia.objects.get(pk=idponencia)
                    #ELIMINACION TOTAL
                    '''ponencia.delete()'''
                    #ELIMINACION LOGICA
                    ponencia.estado = 'ACTIVO'
                    ponencia.save()
                    messages.success(request, 'Ponencia activada con éxito')
                except MaePonencia.DoesNotExist:
                    messages.error(request, 'No se encontró la ponencia')
                except Exception:
                    messages.error(request, 'Error al activar la ponencia')
                return redirect(reverse('RegistrarPonencia', kwargs={'pk':pk}))
            elif action == 'edit':
                idponencia = request.POST.get('id')
                print('Ponente', ponente)
                try:
                    ponencia = MaePonencia.objects.get(pk=idponencia)
                    contexto = {
                        'idponente': ponente,
                        'nombre': nombrePonencia,
                        'idcongreso': MaeCongreso.objects.get(pk=idcongreso)
                    }
                    ponencia_actualizada = PonenciaForm(contexto, instance=ponencia)
                    if ponencia_actualizada.is_valid():
                        ponencia_actualizada.save()
                        messages.success(request, 'Ponencia actualizada con éxito')
                    else:
                        messages.error(request, 'Error al actualizar la ponencia')
                except MaePonencia.DoesNotExist:
                    messages.error(request, 'No se encontró la ponencia')
                except Exception:
                    messages.error(request, 'Error al actualizar la ponencia')
                return redirect(reverse('RegistrarPonencia', kwargs={'pk':pk}))
            
            ponentes = MaePonente.objects.filter(estado='ACTIVO').order_by('pk')
            congresos = MaeCongreso.objects.filter(estado="ACTIVO")
            ponencias = MaePonencia.objects.filter(idcongreso=idcongreso).order_by('pk')
            return render(request, 'pages/registrarPonencia.html', {
                'current_page': 'registrar_ponencia', 
                'ponentes': ponentes, 
                'congresos':congresos,
                'ponencias': ponencias,
                'selected_congreso': int(selected_congreso),
                'pk': pk
            })
        else:
            if not MaePonente.objects.filter(estado="ACTIVO").exists() or not MaePonente.objects.filter().exists():
                messages.warning(request, 'No hay ponentes registrados o activos, registre al menos uno')
            ponencias = MaePonencia.objects.all().order_by('pk')
            congresos = MaeCongreso.objects.filter(estado="ACTIVO")
            return render(request, 'pages/registrarPonencia.html', {
                'current_page': 'registrar_ponencia', 
                'ponencias': ponencias, 
                'congresos':congresos, 
                'selected_congreso': None,
                'pk':pk
            })