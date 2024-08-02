from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from Ponente.models import MaePonente
from Ponente.forms import PonenteForm
from django.contrib import messages

class Registrar_Ponentes(viewsets.ViewSet):
    @method_decorator(login_required)
    def registrar_ponentes(self, request):
        if request.method == 'POST':
            action = request.POST.get('action')
            nombrePonente = request.POST.get('nombres')
            apellidoPonente = request.POST.get('apellidos')
                
            if action == "register":
                try:
                    if (not(MaePonente.objects.filter(nombres=nombrePonente, apellidos=apellidoPonente).exists())):
                        nuevo_ponente = MaePonente(
                            nombres=nombrePonente,
                            apellidos=apellidoPonente,
                        )
                        nuevo_ponente.save()
                        messages.success(request, 'Ponente registrado con éxito')
                    else:
                        messages.error(request, 'El ponente ya existe')
                except Exception:
                    messages.error(request, 'Error al registrar al ponente')
                return redirect('RegistrarPonentes')
            elif action == "delete":
                try:
                    ponente = MaePonente.objects.get(nombres=nombrePonente, apellidos=apellidoPonente)
                    #ELIMINACION TOTAL
                    '''congreso.delete()'''
                    #ELIMINACION LOGICA
                    ponente.estado = "NO ACTIVO"
                    ponente.save()
                    messages.success(request, 'Ponente desactivado con éxito')
                except MaePonente.DoesNotExist:
                    messages.error(request, 'El ponente no existe')
                except Exception:
                    messages.error(request, 'Error al desactivar al ponente')
                return redirect('RegistrarPonentes')
            elif action == "activate":
                try:
                    ponente = MaePonente.objects.get(nombres=nombrePonente, apellidos=apellidoPonente)
                    ponente.estado = "ACTIVO"
                    ponente.save()
                    messages.success(request, 'Ponente activado con éxito')
                except ponente.DoesNotExist:
                    messages.error(request, 'El ponente no existe')
                except Exception:
                    messages.error(request, 'Error al activar al ponente')
                return redirect('RegistrarPonentes')
            elif action == 'edit':
                id_ponente = request.POST.get('id')
                try:
                    ponente = MaePonente.objects.get(pk=id_ponente)
                    contexto = {
                        'nombres': nombrePonente,
                        'apellidos': apellidoPonente,
                    }
                    ponente_actualizado = PonenteForm(contexto, instance=ponente)
                    if ponente_actualizado.is_valid():
                        ponente_actualizado.save()
                        messages.success(request, 'Ponente actualizado con éxito')
                    else:
                        messages.error(request, 'Error al actualizar al ponente')
                except ponente.DoesNotExist:
                    messages.error(request, 'El ponente no existe')
                except Exception:
                    messages.error(request, 'Error al actualizar al ponente')
                return redirect('RegistrarPonentes')

            ponentes = MaePonente.objects.filter().order_by('pk')
            return render(request, 'pages/registrarPonente.html', {
                'current_page': 'registrar_ponentes', 
                'ponentes': ponentes
            })
        else:
            ponentes = MaePonente.objects.all().order_by('pk')
            return render(request, 'pages/registrarPonente.html', {
                'current_page': 'registrar_ponentes', 
                'ponentes': ponentes
            })