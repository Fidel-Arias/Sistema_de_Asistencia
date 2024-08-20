from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from Congreso.models import MaeCongreso
from Colaborador.models import MaeColaborador
from Colaborador.forms import ColaboradorForm
from tipoUsuario.models import MaeTipoUsuario
from ..decorators import administrador_login_required
from django.contrib import messages

class Registrar_Colaboradores(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def registrar_colaboradores(self, request, pk):
        if request.method == 'POST':
            idTipoUsuario = request.POST.get('tipoUsuario')
            nombres = request.POST.get('nombre')
            apellidos = request.POST.get('apellido')
            correo = request.POST.get('correo')
            contrasenia = request.POST.get('contrasenia')
            action = request.POST.get('action')

            if action == 'register':
                try:
                    if (not(MaeColaborador.objects.filter(nombres=nombres, apellidos=apellidos).exists())):
                        nuevo_colaborador = MaeColaborador(
                            nombres=nombres,
                            apellidos=apellidos,
                            correo=correo,
                            contrasenia=contrasenia,
                            idtipo=MaeTipoUsuario.objects.get(pk=idTipoUsuario),
                        )
                        nuevo_colaborador.save()
                        messages.success(request, 'Colaborador registrado con éxito')
                    else:
                        messages.error(request, 'El colaborador registrado ya existe')
                except Exception as e:
                    messages.error(request, 'Error al registrar colaborador')
            elif action == 'delete':
                try:
                    colaborador = MaeColaborador.objects.get(nombres=nombres, apellidos=apellidos)
                    #ELIMINACION TOTAL
                    '''colaborador.delete()'''
                    #ELIMINACION LOGICA
                    colaborador.estado = "NO ACTIVO"
                    colaborador.save()
                    messages.success(request, 'El colaborador ha sido desactivado con éxito')
                except MaeColaborador.DoesNotExist:
                    messages.error(request, 'No se encontró al colaborador')
                except Exception:
                    messages.error(request, 'Error al desactivar al colaborador')
            elif action == 'activate':
                try:
                    colaborador = MaeColaborador.objects.get(nombres=nombres, apellidos=apellidos)
                    colaborador.estado = "ACTIVO"
                    colaborador.save()
                    messages.success(request, 'El colaborador ha sido activado con éxito')
                except MaeColaborador.DoesNotExist:
                    messages.error(request, 'No se encontró al colaborador')
                except Exception:
                    messages.error(request, 'Error al activar al colaborador')
            elif action == 'edit':
                idcolaborador = request.POST.get('id')
                try:
                    colaborador = MaeColaborador.objects.get(pk=idcolaborador)
                    contexto = {
                        'nombres': nombres,
                        'apellidos': apellidos,
                        'correo': correo,
                        'contrasenia': contrasenia,
                        'idtipo': MaeTipoUsuario.objects.get(idtipo=idTipoUsuario),
                    }
                    colaborador_actualizado = ColaboradorForm(contexto, instance=colaborador)
                    if colaborador_actualizado.is_valid():
                        colaborador_actualizado.save()
                        messages.success(request, 'El colaborador se ha actualizado con éxito')
                    else:
                        messages.error(request, 'Error al actualizar al colaborador')
                except MaeColaborador.DoesNotExist:
                    messages.error(request, 'No se encontró al colaborador')
                except Exception as e:
                    messages.error(request, e)

            return redirect(reverse('RegistrarColaboradores', kwargs={'pk':pk}))
        else:
            colaboradores = MaeColaborador.objects.all().order_by('pk')
            if not MaeCongreso.objects.filter(estado='ACTIVO').exists() or not MaeCongreso.objects.filter().exists():
                messages.warning(request, 'No hay congresos registrados o activos, registre al menos uno')
            tiposUsuario = MaeTipoUsuario.objects.filter(dstipo='COLABORADOR')
            return render(request, 'pages/registrarColaboradores.html', {
                'current_page':'registrar_colaboradores', 
                'colaboradores':colaboradores, 
                'tiposUsuario':tiposUsuario, 
                'pk': pk
            })