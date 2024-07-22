from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_framework import viewsets
from .serializers import AdminSerializer
from Asistencia.models import TrsAsistencia
from Asistencia.serializers import AsistenciaSerializer
from Admin.models import MaeAdministrador
from Bloque.models import MaeBloque
from Ponencia.models import MaePonencia
from Dia.models import MaeDia
from Ponente.models import MaePonente
from Ponente.forms import PonenteForm
from CongresoJINIS.models import MaeCongresoJinis
from CongresoJINIS.forms import CongresoJinisForm
from Colaborador.models import MaeColaborador
from tipoUsuario.models import MaeTipoUsuario
from django.contrib import messages
import pandas as pd
from datetime import date

class adminView(viewsets.ViewSet):
    queryset = MaeAdministrador.objects.all()
    serializer_class = AdminSerializer

    def index(self, request):
        contexto = {
            'mensaje': 'Error en la pagina'
        }
        return render(request, 'interfazAdmin.html', contexto)


    def generar_reporte(self, request):
        asistenciaObjetcs = TrsAsistencia.objects.all()
        listaAsistencia = AsistenciaSerializer(asistenciaObjetcs, many=True)
        return render(request, 'pages/generarReporte.html', {'current_page':'generar_reportes', 'listaAsistencia': listaAsistencia.data})
    def registrar_colaboradores(self, request):
        tiposUsuario = MaeTipoUsuario.objects.all()
        bloques = MaeBloque.objects.all()
        congresos = MaeCongresoJinis.objects.all()
        if request.method == 'POST':
            idTipoUsuario = request.POST.get('tipoUsuario')
            idbloque = request.POST.get('bloque')
            idcongreso = request.POST.get('congreso')
            nombreColaborador = request.POST.get('nombre')
            apellidoColaborador = request.POST.get('apellido')
            correoColaborador = request.POST.get('correo')
            contraseniaColaborador = request.POST.get('contrasenia')
            mensaje = ''
            status = 0
            nombreColaborador = nombreColaborador.strip()
            correoColaborador = correoColaborador.strip()
            try:
                if (not(MaeColaborador.objects.filter(nombre=nombreColaborador, apellido=apellidoColaborador, idbloque=idbloque).exists())):
                    nuevo_colaborador = MaeColaborador(
                        nombre=nombreColaborador,
                        apellido=apellidoColaborador,
                        correo=correoColaborador,
                        contrasenia=contraseniaColaborador,
                        idtipo=MaeTipoUsuario.objects.get(pk=idTipoUsuario),
                        idbloque=MaeBloque.objects.get(pk=idbloque),
                        idcongreso=MaeCongresoJinis.objects.get(pk=idcongreso)
                    )
                    nuevo_colaborador.save()
                    mensaje = 'Colaborador registrado con éxito'
                    status = 200
                else:
                    mensaje = 'Ya existe el colaborador en el bloque seleccionado'
                    status = 500
            except Exception as e:
                mensaje = 'Error al registrar colaborador'
                print(e)
                status = 500
            return render(request, 'pages/registrarColaborador.html', {'current_page':'registrar_colaboradores', 'message': mensaje, 'status': status, 'tiposUsuario':tiposUsuario, 'bloques':bloques, 'lista_congresos':congresos})
        else:
            return render(request, 'pages/registrarColaborador.html', {'current_page':'registrar_colaboradores', 'tiposUsuario':tiposUsuario, 'bloques':bloques, 'lista_congresos':congresos})
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
                except ponente.DoesNotExist:
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
            ponentes = MaePonente.objects.all()
            return render(request, 'pages/registrarPonente.html', {'current_page': 'registrar_ponentes', 'ponentes': ponentes})

    def registrar_bloques(self, request):
        lista_ponencias = MaePonencia.objects.all()
        lista_dias = MaeDia.objects.all()
        # hora_final_bd = MaeBloque.objects.last() #Obtiene el ultimo dato ingresado en la base de datos
        if request.method == 'POST':
            ponencia = request.POST.get('ponencia')
            dia = request.POST.get('dia')
            horaInicio = request.POST.get('hora_inicio')
            horaFin = request.POST.get('hora_fin')
            direccion = request.POST.get('direccion')
            if not MaeBloque.objects.filter(idponencia=ponencia).exists(): #verificar el auditorio la hora que se esta ocupando 
                if not MaeBloque.objects.filter(horainicio=horaInicio, horafin=horaFin,  direccion=direccion):
                    
                    try:
                        if horaInicio == horaFin: #mas validaciones validar que bloques se usa el auditorio y comparar con los que se vana ingresar para evitar choques
                            mensaje = "La hora de inicio y fin deben ser diferentes"
                            status = 500
                        elif horaFin < horaInicio:
                            mensaje = "La hora de inicio no puede ser mayor a la hora de fin"
                            status = 500
                        else:
                            nuevo_bloque = MaeBloque(
                                idponencia=MaePonencia.objects.get(idponencia=ponencia),
                                iddia= MaeDia.objects.get(iddia=dia),
                                horainicio=horaInicio,
                                horafin=horaFin,
                                direccion=direccion
                            )
                            nuevo_bloque.save()
                            mensaje = "El bloque ha sido registrado"
                            status = 200
                    except Exception:
                        mensaje = "Error al registara el bloque"
                        status = 500
                    
                else:
                    mensaje = "El auditorio ya esta siendo ocupado en la hora indicada"
                    status = 500
            else:
                mensaje = "El bloque con la ponencia ya existe"
                status = 500
            return render(request, 'pages/registrarBloques.html', {'current_page': 'registrar_bloques', 'ponencias': lista_ponencias, 'dias': lista_dias, 'message': mensaje, 'status': status})
        else:
            if (not(MaePonencia.objects.exists())):
                mensaje = 'No hay ponencias registradas, por favor registre al menos una'
                status = 500
                return render(request, 'pages/registrarBloques.html', {'current_page':'registrar_bloques', 'message': mensaje, 'status': status, 'dias': lista_dias})
            elif (not(MaeDia.objects.exists())):
                mensaje = 'No hay días registrados, por favor registre al menos un día'
                status = 500
                return render(request, 'pages/registrarBloques.html', {'current_page':'registrar_bloques', 'message': mensaje, 'status': status, 'ponencias': lista_dias})
            else:
                return render(request, 'pages/registrarBloques.html', {'current_page': 'registrar_bloques', 'ponencias': lista_ponencias, 'dias': lista_dias})
    def registrar_ponencia(self, request):
        ponentes = MaePonente.objects.all()
        if request.method == 'POST':
            action = request.POST.get('action')
            print('action: ' + action)
            ponente = request.POST.get('ponente')
            nombrePonencia = request.POST.get('nombre_ponencia')
            print("Ponente seleccionado:", ponente)
            print("Ponencia seleccionado:", nombrePonencia)
            try:
                if (not(MaePonencia.objects.filter(nombre=nombrePonencia).exists())):
                    nueva_ponencia = MaePonencia(
                        nombre=nombrePonencia,
                        idponente=MaePonente.objects.get(pk=ponente)
                    )
                    nueva_ponencia.save()
                    mensaje = 'Ponencia registrada con éxito'
                    status = 200
                else:
                    mensaje = 'Ya existe la ponencia'
                    status = 500
                return render(request, 'pages/registrarPonencia.html', {'current_page':'registrar_ponencia', 'message': mensaje, 'status':status, 'ponentes': ponentes})
            except Exception:
                mensaje = 'Error al registrar la ponencia'
                status = 500
                return render(request, 'pages/registrarPonencia.html', {'current_page':'registrar_ponencia', 'message': mensaje, 'status':status, 'ponentes': ponentes})
        else:
            if ((MaePonente.objects.exists())):
                status = 200
                return render(request, 'pages/registrarPonencia.html', {'current_page': 'registrar_ponencia', 'ponentes':ponentes, 'status':status})
            else:
                mensaje = 'No hay ponentes registrados'
                status = 501
                return render(request, 'pages/registrarPonencia.html', {'current_page': 'registrar_ponencia', 'message': mensaje, 'status': status})
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
            congresos = MaeCongresoJinis.objects.all()
            return render(request, 'pages/registrarCongreso.html', {'current_page': 'registrar_congreso', 'congresos':congresos})

    def cerrar_sesion(request):
        return render(request, 'loginAdmin.html', {'current_page': 'cerrar_sesion'})
    

def ingresoAdmin(request):
    correoAdmin = request.POST.get('correo')
    contraseniaAdmin = request.POST.get('contrasenia')
    try:
        admin = MaeAdministrador.objects.get(correo=correoAdmin, contrasenia=contraseniaAdmin)
        return render(request, 'interfazBienvenida.html', {'admin': admin})
    except MaeAdministrador.DoesNotExist:
        return redirect(reverse('LoguingAdministrador') + '?error=Usuario-o-contraseña-incorrectos')
    
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



        