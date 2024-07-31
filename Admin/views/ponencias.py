from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Ponencia.models import MaePonencia
from Ponencia.forms import PonenciaForm
from Ponente.models import MaePonente
from CongresoJINIS.models import MaeCongresoJinis
from django.contrib import messages

@login_required
def registrar_ponencia(request):
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
                        idcongreso=MaeCongresoJinis.objects.get(pk=idcongreso)
                    )
                    nueva_ponencia.save()
                    messages.success(request, 'Ponencia registrada con éxito')
                else:
                    messages.error(request, 'Ya existe la ponencia')
            except Exception:
                messages.error(request, 'Error al registrar la ponencia')
            return redirect('RegistrarPonencia')
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
            return redirect('RegistrarPonencia')
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
            return redirect('RegistrarPonencia')
        elif action == 'edit':
            idponencia = request.POST.get('id')
            print('Ponente', ponente)
            try:
                ponencia = MaePonencia.objects.get(pk=idponencia)
                contexto = {
                    'idponente': ponente,
                    'nombre': nombrePonencia,
                    'idcongreso': MaeCongresoJinis.objects.get(pk=idcongreso)
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
            return redirect('RegistrarPonencia')
        
        ponentes = MaePonente.objects.filter(idcongreso=int(idcongreso), estado='ACTIVO').order_by('pk')
        congresos = MaeCongresoJinis.objects.filter(estado="ACTIVO")
        ponencias = MaePonencia.objects.filter(idcongreso=idcongreso).order_by('pk')
        return render(request, 'pages/registrarPonencia.html', {
            'current_page': 'registrar_ponencia', 
            'ponentes': ponentes, 
            'congresos':congresos,
            'ponencias': ponencias,
            'selected_congreso': int(selected_congreso)
        })
    else:
        if not MaePonente.objects.filter(estado="ACTIVO").exists() or not MaePonente.objects.filter().exists():
            messages.warning(request, 'No hay ponentes registrados o activos, registre al menos uno')
        ponencias = MaePonencia.objects.all().order_by('pk')
        congresos = MaeCongresoJinis.objects.filter(estado="ACTIVO")
        return render(request, 'pages/registrarPonencia.html', {
            'current_page': 'registrar_ponencia', 
            'ponencias': ponencias, 
            'congresos':congresos, 
            'selected_congreso': None
        })