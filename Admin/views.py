from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import connection, transaction
from rest_framework import viewsets
from Asistencia.models import TrsAsistencia
from Asistencia.serializers import AsistenciaSerializer
from Admin.models import MaeAdministrador
from Bloque.models import MaeBloque
from Bloque.forms import BloqueForm
from Ponencia.models import MaePonencia
from Ponencia.forms import PonenciaForm
from Dia.models import MaeDia
from Ponente.models import MaePonente
from Ponente.forms import PonenteForm
from CongresoJINIS.models import MaeCongresoJinis
from CongresoJINIS.forms import CongresoJinisForm
from Colaborador.models import MaeColaborador
from Colaborador.forms import ColaboradorForm
from tipoUsuario.models import MaeTipoUsuario
from Ubicacion.models import MaeUbicacion
from Ubicacion.forms import UbicacionForm
from BloqueColaborador.models import BloqueColaborador
from django.contrib import messages
import pandas as pd
from datetime import date

class adminView(viewsets.ViewSet):

    def index(self, request):
        contexto = {
            'mensaje': 'Error en la pagina'
        }
        return render(request, 'interfazAdmin.html', contexto)


    def generar_reporte(self, request):
        asistenciaObjetcs = TrsAsistencia.objects.all().order_by('pk')
        listaAsistencia = AsistenciaSerializer(asistenciaObjetcs, many=True)
        return render(request, 'pages/generarReporte.html', {'current_page':'generar_reportes', 'listaAsistencia': listaAsistencia.data})
    def registrar_cargos_usuarios(self, request):
        if request.method == 'POST':
            idTipoUsuario = request.POST.get('tipoUsuario')
            idcongreso = request.POST.get('congreso')
            nombreColaborador = request.POST.get('nombre')
            apellidoColaborador = request.POST.get('apellido')
            correoColaborador = request.POST.get('correo')
            contraseniaColaborador = request.POST.get('contrasenia')
            action = request.POST.get('action')
            if action == 'register':
                try:
                    if (not(MaeColaborador.objects.filter(nombre=nombreColaborador, apellido=apellidoColaborador).exists())):
                        nuevo_colaborador = MaeColaborador(
                            nombre=nombreColaborador,
                            apellido=apellidoColaborador,
                            correo=correoColaborador,
                            contrasenia=contraseniaColaborador,
                            idtipo=MaeTipoUsuario.objects.get(pk=idTipoUsuario),
                            idcongreso=MaeCongresoJinis.objects.get(pk=idcongreso)
                        )
                        nuevo_colaborador.save()
                        messages.success(request, 'Colaborador registrado con éxito')
                    else:
                        messages.error(request, 'El colaborador registrado ya existe')
                except Exception as e:
                    messages.error(request, 'Error al registrar colaborador')
                return redirect('RegistrarCargosUsuarios')
            elif action == 'delete':
                try:
                    colaborador = MaeColaborador.objects.get(nombre=nombreColaborador, apellido=apellidoColaborador)
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
                return redirect('RegistrarCargosUsuarios')
            elif action == 'activate':
                try:
                    colaborador = MaeColaborador.objects.get(nombre=nombreColaborador, apellido=apellidoColaborador)
                    colaborador.estado = "ACTIVO"
                    colaborador.save()
                    messages.success(request, 'El colaborador ha sido activado con éxito')
                except MaeColaborador.DoesNotExist:
                    messages.error(request, 'No se encontró al colaborador')
                except Exception:
                    messages.error(request, 'Error al activar al colaborador')
                return redirect('RegistrarCargosUsuarios')
            elif action == 'edit':
                idcolaborador = request.POST.get('id')
                try:
                    colaborador = MaeColaborador.objects.get(pk=idcolaborador)
                    contexto = {
                        'nombre': nombreColaborador,
                        'apellido': apellidoColaborador,
                        'correo': correoColaborador,
                        'contrasenia': contraseniaColaborador,
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
        else:
            colaboradores = MaeColaborador.objects.all().order_by('pk')
            if not MaeCongresoJinis.objects.filter(estado='ACTIVO').exists() or not MaeCongresoJinis.objects.filter().exists():
                messages.warning(request, 'No hay congresos registrados o activos, registre al menos uno')
            tiposUsuario = MaeTipoUsuario.objects.all().order_by('pk')
            congresos = MaeCongresoJinis.objects.all().order_by('pk')
            return render(request, 'pages/registrarCargosUsuario.html', {'current_page':'registrar_cargos_usuarios', 'colaboradores':colaboradores, 'tiposUsuario':tiposUsuario, 'lista_congresos':congresos})
    def registrar_ponentes(self, request):
        if request.method == 'POST':
            action = request.POST.get('action')
            nombrePonente = request.POST.get('nombre')
            apellidoPonente = request.POST.get('apellido')
            if action == "register":
                try:
                    if (not(MaePonente.objects.filter(nombre=nombrePonente, apellido=apellidoPonente).exists())):
                        nuevo_ponente = MaePonente(
                            nombre=nombrePonente,
                            apellido=apellidoPonente
                        )
                        nuevo_ponente.save()
                        messages.success(request, 'Ponente registrado con éxito')
                    else:
                        messages.error(request, 'El ponente ya existe')
                except Exception:
                    messages.error(request, 'Error al registrar ponente')
                return redirect('RegistrarPonentes')
            elif action == "delete":
                try:
                    ponente = MaePonente.objects.get(nombre=nombrePonente, apellido=apellidoPonente)
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
                    ponente = MaePonente.objects.get(nombre=nombrePonente, apellido=apellidoPonente)
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
                        'nombre': nombrePonente,
                        'apellido': apellidoPonente
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
        else:
            ponentes = MaePonente.objects.all().order_by('pk')
            return render(request, 'pages/registrarPonente.html', {'current_page': 'registrar_ponentes', 'ponentes': ponentes})

    def registrar_bloques(self, request):
        # hora_final_bd = MaeBloque.objects.last() #Obtiene el ultimo dato ingresado en la base de datos
        if request.method == 'POST':
            ponencia = request.POST.get('ponencia')
            dia = request.POST.get('dia')
            horaInicio = request.POST.get('hora_inicio')
            horaFin = request.POST.get('hora_fin')
            ubicacion = request.POST.get('ubicacion')
            action = request.POST.get('action')
            if action == 'register':
                if not MaeBloque.objects.filter(idponencia=ponencia).exists():
                    try:
                        if horaInicio == horaFin: #mas validaciones validar que bloques se usa el auditorio y comparar con los que se vana ingresar para evitar choques
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
                return redirect('RegistrarBloques')
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
                return redirect('RegistrarBloques')
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
                return redirect('RegistrarBloques')
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
                return redirect('RegistrarBloques')
        else:
            bloques = MaeBloque.objects.filter().order_by('pk')
            if not MaePonencia.objects.filter(estado='ACTIVO').exists() or not MaePonencia.objects.filter().exists():
                messages.warning(request,'No hay ponencias registradas o activas, por favor registre al menos una')
            elif not MaeDia.objects.filter(estado='ACTIVO').exists() or not MaeDia.objects.filter().exists():
                messages.warning(request, 'No hay días registrados o activos, por favor registre al menos un día')
            elif not MaeUbicacion.objects.filter(estado='ACTIVO').exists() or not MaeUbicacion.objects.filter().exists():
                messages.warning(request, 'No hay ubicaciones registradas o activas, por favor registre al menos una ubicación')
            
            lista_ponencias = MaePonencia.objects.filter(estado='ACTIVO').order_by('pk')
            lista_dias = MaeDia.objects.filter(estado='ACTIVO').order_by('pk')
            ubicaciones = MaeUbicacion.objects.filter(estado='ACTIVO').order_by('pk')
            return render(request, 'pages/registrarBloques.html', {'current_page': 'registrar_bloques', 'ponencias': lista_ponencias, 'dias': lista_dias, 'ubicaciones':ubicaciones, 'bloques':bloques})
    def registrar_ponencia(self, request):
        if request.method == 'POST':
            action = request.POST.get('action')
            ponente = request.POST.get('ponente')
            nombrePonencia = request.POST.get('nombre_ponencia')
            if action == 'register':
                try:
                    if (not(MaePonencia.objects.filter(nombre=nombrePonencia).exists())):
                        nueva_ponencia = MaePonencia(
                            nombre=nombrePonencia,
                            idponente=MaePonente.objects.get(pk=ponente)
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
                        'nombre': nombrePonencia
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
        else:
            if not MaePonente.objects.filter(estado="ACTIVO").exists() or not MaePonente.objects.filter().exists():
                messages.warning(request, 'No hay ponentes registrados o activos, registre al menos uno')
            ponencias = MaePonencia.objects.all().order_by('pk')
            ponentes = MaePonente.objects.filter(estado="ACTIVO")
            return render(request, 'pages/registrarPonencia.html', {'current_page': 'registrar_ponencia', 'ponentes':ponentes, 'ponencias': ponencias})
    def registrar_congreso(self, request):
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
                        if (not(MaeCongresoJinis.objects.filter(nombre=nombreCongreso).exists())):
                            nueva_congreso = MaeCongresoJinis(
                                nombre=nombreCongreso,
                                fechainicio=fechaInicio,
                                fechafin=fechaFin,
                                asistenciatotal=asistenciaTotal
                            )
                            nueva_congreso.save()
                            generacion_ingreso_tabla_dias(request, fechaInicio, fechaFin)
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
                    messages.success(request, 'Congreso desactivado con éxito')
                except MaeCongresoJinis.DoesNotExist:
                    messages.error(request, 'No se encontró el congreso')
                except Exception:
                    messages.error(request, 'Error al eliminar el congreso')
                return redirect('RegistrarCongreso')
            elif action == 'activate':
                try:
                    congreso = MaeCongresoJinis.objects.get(nombre=nombreCongreso)
                    congreso.estado = 'ACTIVO'
                    congreso.save()
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
                        # generacion_ingreso_tabla_dias(request, fechaInicio, fechaFin)
                        messages.success(request, 'Congreso actualizado con éxito')
                    else:
                        messages.error(request, congreso_actualizado.errors)
                except MaeCongresoJinis.DoesNotExist:
                    messages.error(request, 'El congreso ya no existe')
                return redirect('RegistrarCongreso')
        else:
            congresos = MaeCongresoJinis.objects.all().order_by('pk')
            return render(request, 'pages/registrarCongreso.html', {'current_page': 'registrar_congreso', 'congresos':congresos})

    def registrar_ubicacion(self, request):
        if request.method == 'POST':
            nombreUbicacion = request.POST.get('nombre_ubicacion')
            action = request.POST.get('action')
            if action == 'register':
                try:
                    if (not(MaeUbicacion.objects.filter(nombre=nombreUbicacion).exists())):
                        nueva_ubicacion = MaeUbicacion(
                            nombre=nombreUbicacion,
                        )
                        nueva_ubicacion.save()
                        messages.success(request, 'Ubicación registrada con éxito')
                    else:
                        messages.error(request, 'Ya existe la ubicación')
                except Exception:
                    messages.error(request, 'Error al registrar la ubicación')
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
            return render(request, 'pages/registrarUbicaciones.html', {'current_page': 'registrar_ubicaciones', 'ubicaciones':ubicaciones})
    
    def registrar_bloques_colaboradores(self, request):
        if request.method == 'POST':
            colaborador = request.POST.get('colaborador')
            bloques = request.POST.getlist('bloques')
            action = request.POST.get('action')
            if action == 'register':
                try:
                    if (not(BloqueColaborador.objects.filter(idcolaborador=colaborador).exists())):
                        with transaction.atomic():
                            for i in range(0, len(bloques)):
                                nuevo_bloqueColaborador = BloqueColaborador(
                                    idcolaborador=MaeColaborador.objects.get(pk=colaborador),
                                    idbloque=MaeBloque.objects.get(pk=bloques[i]),
                                )
                                nuevo_bloqueColaborador.save()
                            messages.success(request, 'Se registró exitosamente los bloques del colaborador')
                    else:
                        messages.error(request, 'Ya existe el colaborador con sus bloques')
                except BloqueColaborador.DoesNotExist:
                    messages.error(request, 'No se encontró al colaborador o a los bloques')
                except Exception as e:    
                    messages.error(request, e) #unsupported operand type(s) for +: 'int' and 'str'
                return redirect('RegistrarBloqueColaborador')
            elif action == 'delete':
                try:
                    bloques_colaborador = BloqueColaborador.objects.filter(idcolaborador=colaborador)
                    with transaction.atomic():
                        for bloque_colaborador in bloques_colaborador:
                            bloque_colaborador.estado = 'NO ACTIVO'
                            bloque_colaborador.save()
                    messages.success(request, 'Bloque del colaborador desactivado con éxito')
                except BloqueColaborador.DoesNotExist:
                    messages.error(request, 'No se encontró al colaborador o al bloque')
                except Exception as e:    
                    messages.error(request, e)
                return redirect('RegistrarBloqueColaborador')
            elif action == 'activate':
                try:
                    bloques_colaborador = BloqueColaborador.objects.filter(idcolaborador=colaborador)
                    with transaction.atomic():
                        for bloque_colaborador in bloques_colaborador:
                            bloque_colaborador.estado = 'ACTIVO'
                            bloque_colaborador.save()
                    messages.success(request, 'Bloque del colaborador activado con éxito')
                except BloqueColaborador.DoesNotExist:
                    messages.error(request, 'No se encontró al colaborador o al bloque')
                except Exception:    
                    messages.error(request, 'Error al activar el bloque del colaborador') #unsupported operand type(s) for +: 'int' and 'str'
                return redirect('RegistrarBloqueColaborador')
            elif action == 'edit':
                idblcl = request.POST.get('id')
                try:
                    bloque_colaborador = BloqueColaborador.objects.get(pk=idblcl)
                    colaborador_obj = MaeColaborador.objects.get(pk=colaborador)

                    # Eliminar los bloques actuales del colaborador
                    BloqueColaborador.objects.filter(idcolaborador=colaborador_obj).delete()
                    # Agregar los nuevos bloques seleccionados
                    with transaction.atomic():
                        # Agregar los nuevos bloques seleccionados
                        for i in range(len(bloques)):
                            nuevo_bloqueColaborador = BloqueColaborador(
                                idcolaborador=colaborador_obj,
                                idbloque=MaeBloque.objects.get(pk=bloques[i]),
                            )
                            nuevo_bloqueColaborador.save()
                        messages.success(request, 'Bloques del colaborador actualizado con éxito')
                except BloqueColaborador.DoesNotExist:
                    messages.error(request, 'No se encontró al colaborador o al bloque')
                return redirect('RegistrarBloqueColaborador')
        else:
            if not MaeColaborador.objects.filter(estado='ACTIVO').exists() or not MaeColaborador.objects.filter().exists():
                messages.warning(request, 'No hay colaboradores registrados o activos, registre al menos uno')
            elif not MaeBloque.objects.filter(estado='ACTIVO').exists() or not MaeBloque.objects.filter().exists():
                messages.warning(request, 'No hay bloques registrados o activos, registre al menos uno')
            colaboradores = MaeColaborador.objects.filter(estado='ACTIVO').order_by('pk')
            bloques = MaeBloque.objects.filter(estado='ACTIVO').order_by('pk')
                
            bloquesToColaboradores = BloqueColaborador.objects.all().order_by('pk')

            # Agrupar bloques por colaborador
            bloques_por_colaborador = defaultdict(list)
            for blcl in bloquesToColaboradores:
                bloques_por_colaborador[blcl.idcolaborador].append(blcl)
            return render(request, 'pages/bloqueColaborador.html', {'current_page': 'registrar_bloques_colaboradores', 'bloques_por_colaborador':dict(bloques_por_colaborador), 'colaboradores': colaboradores, 'bloques':bloques})
    

def ingresoAdmin(request):
    if request.method == 'POST':
        correoAdmin = request.POST.get('correo')
        contraseniaAdmin = request.POST.get('contrasenia')
        try:
            admin = MaeAdministrador.objects.get(correo=correoAdmin, contrasenia=contraseniaAdmin)
            request.session['correo_admin'] = admin.correo
            request.session['contrasenia_admin'] = admin.contrasenia
            return redirect('Administrador')
        except MaeAdministrador.DoesNotExist:
            return redirect(reverse('LoguingAdministrador') + '?error=Usuario-o-contraseña-incorrectos')
    else:
        correoAdmin = request.session.get('correo_admin')
        contraseniaAdmin = request.session.get('contrasenia_admin')
        admin = MaeAdministrador.objects.get(correo=correoAdmin, contrasenia=contraseniaAdmin)
        return render(request, 'interfazBienvenida.html', {'admin': admin})
    
def generacion_ingreso_tabla_dias(request, fechaInicio, fechaFin):
    try:
        date_range = pd.date_range(start=fechaInicio, end=fechaFin) #Generación de rangos desde la fecha de inicio hasta la fecha fin
        date_list = date_range.strftime('%Y-%m-%d').tolist()
        lista_dias = None
        for i in range(0, len(date_list)):
            lista_dias = MaeDia(
                fecha = date_list[i]
            )
            lista_dias.save()
    except Exception:
        messages.error(request, 'Error en la generación de días')
        return redirect('RegistrarCongreso')

def verificar_ubicacion(id, fecha, hora_inicio, hora_fin, ubicacion):
    cursor = connection.cursor()
    cursor.callproc('verificar_ubicacion', [id, fecha, hora_inicio, hora_fin, ubicacion])
    resultado = cursor.fetchone()[0]
    return resultado
