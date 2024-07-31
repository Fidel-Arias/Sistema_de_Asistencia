from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Ubicacion.models import MaeUbicacion
from Ubicacion.forms import UbicacionForm
from django.contrib import messages

@login_required
def registrar_ubicacion(request):
    if request.method == 'POST':
        nombreUbicacion = request.POST.get('nombre_ubicacion')
        action = request.POST.get('action')
        if action == 'register':
            try:
                if (not(MaeUbicacion.objects.filter(ubicacion=nombreUbicacion).exists())):
                    nueva_ubicacion = MaeUbicacion(
                        ubicacion=nombreUbicacion,
                    )
                    nueva_ubicacion.save()
                    messages.success(request, 'Ubicación registrada con éxito')
                else:
                    messages.error(request, 'Ya existe la ubicación')
            except Exception as e: #Cannot resolve keyword 'nombre' into field. Choices are: estado, idubicacion, maebloque, ubicacion
                messages.error(request, e)
            return redirect('RegistrarUbicaciones')
        elif action == 'delete':
            try:
                ubicacion = MaeUbicacion.objects.get(ubicacion=nombreUbicacion)
                #ELIMINACION TOTAL
                '''ubicacion.delete()'''
                #ELIMINACION LOGICA
                ubicacion.estado = 'NO ACTIVO'
                ubicacion.save()
                messages.success(request, 'Ubicación desactivada con éxito')
            except MaeUbicacion.DoesNotExist:
                messages.error(request, 'No se encontró la ubicación')
            except Exception:
                messages.error(request, 'Error al desactivar la ubicación')
            return redirect('RegistrarUbicaciones')
        elif action == 'activate':
            try:
                ubicacion = MaeUbicacion.objects.get(ubicacion=nombreUbicacion)
                ubicacion.estado = 'ACTIVO'
                ubicacion.save()
                messages.success(request, 'Ubicación activada con éxito')
            except MaeUbicacion.DoesNotExist:
                messages.error(request, 'No se encontró la ubicación')
            except Exception:
                messages.error(request, 'Error al activar la ubicación')
            return redirect('RegistrarUbicaciones')
        elif action == 'edit':
            idubicacion = request.POST.get('id')
            try:
                ubicacion = MaeUbicacion.objects.get(pk=idubicacion)
                contexto = {
                    'ubicacion': nombreUbicacion,
                }
                ubicacion_actualizada = UbicacionForm(contexto, instance=ubicacion)
                if ubicacion_actualizada.is_valid():
                    ubicacion_actualizada.save()
                    messages.success(request, 'Ubicación actualizada con éxito')
                else:
                    messages.error(request, 'Error al actualizar la ubicación')
            except MaeUbicacion.DoesNotExist:
                messages.error(request, 'La ubicación ya no existe')
            except Exception:
                messages.error(request, 'Error al actualizar la ubicación')
            return redirect('RegistrarUbicaciones')
    else:
        ubicaciones = MaeUbicacion.objects.all().order_by('pk')
        return render(request, 'pages/registrarUbicaciones.html', {
            'current_page': 'registrar_ubicaciones', 
            'ubicaciones':ubicaciones
        })