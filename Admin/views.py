from django.shortcuts import render, redirect
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
from CongresoJINIS.models import MaeCongresoJinis
from Colaborador.models import MaeColaborador
from tipoUsuario.models import MaeTipoUsuario
from Bloque.serializers import BloqueSerializer
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
            nombrePonente = request.POST.get('nombre')
            apellidoPonente = request.POST.get('apellido')
            mensaje = ''
            status = 0
            nombrePonente = nombrePonente.strip()
            apellidoPonente = apellidoPonente.strip()
            try:
                if (not(MaePonente.objects.filter(nombre=nombrePonente, apellido=apellidoPonente).exists())):
                    nuevo_ponente = MaePonente(
                        nombre=nombrePonente,
                        apellido=apellidoPonente
                    )
                    nuevo_ponente.save()
                    mensaje = 'Ponente registrado con éxito'
                    status = 200
                else:
                    mensaje = 'Ya existe el ponente'
                    status = 500
                return render(request, 'pages/registrarPonente.html', {'current_page': 'registrar_ponentes', 'message': mensaje, 'status': status})
            except Exception:
                mensaje = 'Error al registrar ponente'
                status = 500
                return render(request, 'pages/registrarPonente.html', {'current_page': 'registrar_ponentes', 'message': mensaje, 'status': status})
        else:
            return render(request, 'pages/registrarPonente.html', {'current_page': 'registrar_ponentes'})

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
            nombreCongreso = request.POST.get('nombreCongreso')
            fechaHoy = date.today()
            fechaInicio = request.POST.get('fechaInicio')
            fechaFin = request.POST.get('fechaFin')
            if fechaInicio == fechaFin:
                mensaje = 'Las fechas de inicio y fin deben ser distintas'
                status = 500
                return render(request, 'pages/registrarCongreso.html', {'current_page':'registrar_congreso', 'message': mensaje, 'status': status})
            elif fechaFin < fechaInicio:
                mensaje = 'Ingrese correctamente las fechas'
                status = 500
                return render(request, 'pages/registrarCongreso.html', {'current_page':'registrar_congreso', 'message': mensaje, 'status': status})
            elif fechaInicio < fechaHoy.__str__() or fechaFin < fechaHoy.__str__():
                mensaje = 'La fecha de inicio y fin no puede ser anterior a la fecha de hoy'
                status = 500
                return render(request, 'pages/registrarCongreso.html', {'current_page':'registrar_congreso', 'message': mensaje, 'status': status})
            else:
                try:
                    if (not(MaeCongresoJinis.objects.filter(nombre=nombreCongreso).exists())):
                        nueva_congreso = MaeCongresoJinis(
                            nombre=nombreCongreso,
                            fechainicio=fechaInicio,
                            fechafin=fechaFin
                        )
                        nueva_congreso.save()
                        mensaje = 'Congreso registrado con éxito'
                        status = 200
                        generacion_ingreso_tabla_dias(request, fechaInicio, fechaFin)
                    else:
                        mensaje = 'Ya existe el congreso'
                        status = 500
                except Exception:
                    mensaje = 'Error al registrar el congreso'
                    status = 500
                return render(request, 'pages/registrarCongreso.html', {'current_page':'registrar_congreso', 'message': mensaje, 'status': status})
        else:
            return render(request, 'pages/registrarCongreso.html', {'current_page': 'registrar_universidades'})

    def cerrar_sesion(request):
        return render(request, 'loginAdmin.html', {'current_page': 'cerrar_sesion'})
    

def ingresoAdmin(request):
    correoAdmin = request.POST.get('correo')
    contraseniaAdmin = request.POST.get('contrasenia')
    try:
        admin = MaeAdministrador.objects.get(correo=correoAdmin, contrasenia=contraseniaAdmin)
        request.session['correoAdmin'] = correoAdmin
        request.session['contraseniaAdmin'] = contraseniaAdmin
        serializer = AdminSerializer(admin)
        return render(request, 'interfazAdmin.html', serializer.data)
    except MaeAdministrador.DoesNotExist:
        print("No existe chavo")
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
        mensaje = 'Error en la generación de días'
        status = 500
        return render(request, 'pages/registrarCongreso.html', {'current_page':'registrar_congreso', 'message': mensaje, 'status': status})



        