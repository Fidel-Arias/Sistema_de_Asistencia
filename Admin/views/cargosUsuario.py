from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from CongresoJINIS.models import MaeCongresoJinis
from Colaborador.models import MaeColaborador
from Colaborador.forms import ColaboradorForm
from tipoUsuario.models import MaeTipoUsuario
from Admin.models import MaeAdministrador
from Admin.forms import AdministradorForm
from django.contrib import messages

@login_required
def registrar_cargos_usuarios(request):
    if request.method == 'POST':
        idTipoUsuario = request.POST.get('tipoUsuario')
        idcongreso = request.POST.get('congreso')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        contrasenia = request.POST.get('contrasenia')
        action = request.POST.get('action')

        if idcongreso:
            selected_congreso = idcongreso
        else:
            selected_congreso = None

        if idTipoUsuario:
            TipoUsuario = MaeTipoUsuario.objects.get(pk=idTipoUsuario)
            print('usuario: ', TipoUsuario)
            if TipoUsuario.dstipo == "COLABORADOR":
                if action == 'register':
                    try:
                        if (not(MaeColaborador.objects.filter(nombre=nombre, apellido=apellido).exists())):
                            nuevo_colaborador = MaeColaborador(
                                nombre=nombre,
                                apellido=apellido,
                                correo=correo,
                                contrasenia=contrasenia,
                                idtipo=MaeTipoUsuario.objects.get(pk=idTipoUsuario),
                                idcongreso=MaeCongresoJinis.objects.get(pk=idcongreso)
                            )
                            nuevo_colaborador.save()
                            messages.success(request, 'Colaborador registrado con éxito')
                        else:
                            messages.error(request, 'El colaborador registrado ya existe')
                    except Exception as e:
                        messages.error(request, 'Error al registrar colaborador')
                elif action == 'delete':
                    try:
                        colaborador = MaeColaborador.objects.get(nombre=nombre, apellido=apellido)
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
                        colaborador = MaeColaborador.objects.get(nombre=nombre, apellido=apellido)
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
                            'nombre': nombre,
                            'apellido': apellido,
                            'correo': correo,
                            'contrasenia': contrasenia,
                            'idtipo': MaeTipoUsuario.objects.get(idtipo=idTipoUsuario),
                            'idcongreso': MaeCongresoJinis.objects.get(idcongreso=idcongreso)
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

                return redirect('RegistrarCargosUsuarios')
            
            elif TipoUsuario.dstipo == "ADMINISTRADOR":
                if action == 'register':
                    try:
                        if (not(MaeAdministrador.objects.filter(nombre=nombre, apellido=apellido).exists())):
                            nuevo_admin = MaeAdministrador(
                                nombre=nombre,
                                apellido=apellido,
                                correo=correo,
                                contrasenia=contrasenia,
                                idtipo=MaeTipoUsuario.objects.get(pk=idTipoUsuario),
                                idcongreso=MaeCongresoJinis.objects.get(pk=idcongreso)
                            )
                            nuevo_admin.save()
                            messages.success(request, 'Administrador registrado con éxito')
                        else:
                            messages.error(request, 'El administrador registrado ya existe')
                    except Exception:
                        messages.error(request, 'Error al registrar al administrador')
                elif action == 'delete':
                    try:
                        administrador = MaeAdministrador.objects.get(nombre=nombre, apellido=apellido)
                        #ELIMINACION TOTAL
                        '''colaborador.delete()'''
                        #ELIMINACION LOGICA
                        administrador.estado = "NO ACTIVO"
                        administrador.save()
                        messages.success(request, 'El administrador ha sido desactivado con éxito')
                    except MaeAdministrador.DoesNotExist:
                        messages.error(request, 'No se encontró al administrador')
                    except Exception:
                        messages.error(request, 'Error al desactivar al colaborador')
                elif action == 'activate':
                    try:
                        administrador = MaeAdministrador.objects.get(nombre=nombre, apellido=apellido)
                        administrador.estado = "ACTIVO"
                        administrador.save()
                        messages.success(request, 'El colaborador ha sido activado con éxito')
                    except MaeAdministrador.DoesNotExist:
                        messages.error(request, 'No se encontró al colaborador')
                    except Exception:
                        messages.error(request, 'Error al activar al colaborador')
                elif action == 'edit':
                    idadministrador = request.POST.get('id')
                    try:
                        administrador = MaeAdministrador.objects.get(pk=idadministrador)
                        contexto = {
                            'nombre': nombre,
                            'apellido': apellido,
                            'correo': correo,
                            'contrasenia': contrasenia,
                            'idtipo': MaeTipoUsuario.objects.get(idtipo=idTipoUsuario),
                            'idcongreso': MaeCongresoJinis.objects.get(idcongreso=idcongreso)
                        }
                        administrador_actualizado = AdministradorForm(contexto, instance=administrador)
                        if administrador_actualizado.is_valid():
                            administrador_actualizado.save()
                            messages.success(request, 'El administrador se ha actualizado con éxito')
                        else:
                            messages.error(request, 'Error al actualizar al administrador')
                    except MaeAdministrador.DoesNotExist:
                        messages.error(request, 'No se encontró al administrador')
                    except Exception as e:
                        messages.error(request, e)
                return redirect('RegistrarCargosUsuarios')
            
        colaboradores = MaeColaborador.objects.filter(idcongreso=idcongreso).order_by('pk')
        administradores = MaeAdministrador.objects.filter(idcongreso=idcongreso).order_by('pk')
        tiposUsuario = MaeTipoUsuario.objects.all().order_by('pk')
        congresos = MaeCongresoJinis.objects.all().order_by('pk')
        return render(request, 'pages/registrarCargosUsuario.html', {
            'current_page':'registrar_cargos_usuarios', 
            'colaboradores':colaboradores, 
            'administradores': administradores,
            'tiposUsuario':tiposUsuario, 
            'congresos':congresos, 
            'administradores':administradores,
            'selected_congreso': int(selected_congreso)
        })
    else:
        colaboradores = MaeColaborador.objects.all().order_by('pk')
        administradores = MaeAdministrador.objects.all().order_by('pk')
        if not MaeCongresoJinis.objects.filter(estado='ACTIVO').exists() or not MaeCongresoJinis.objects.filter().exists():
            messages.warning(request, 'No hay congresos registrados o activos, registre al menos uno')
        tiposUsuario = MaeTipoUsuario.objects.all().order_by('pk')
        congresos = MaeCongresoJinis.objects.all().order_by('pk')
        return render(request, 'pages/registrarCargosUsuario.html', {
            'current_page':'registrar_cargos_usuarios', 
            'colaboradores':colaboradores, 
            'tiposUsuario':tiposUsuario, 
            'congresos':congresos, 
            'administradores':administradores,
            'selected_congreso': None,
        })