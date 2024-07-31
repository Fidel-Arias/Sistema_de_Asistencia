from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import MaeColaborador
from Bloque.models import MaeBloque
from CongresoJINIS.models import MaeCongresoJinis
from Asistencia.models import TrsAsistencia
from Bloque.models import MaeBloque
from CongresoJINIS.models import MaeCongresoJinis
from datetime import date

class LoginColaborador(View):
    def get(self, request):
        error = request.session.pop('error', None)  # Obtiene y elimina el mensaje de error de la sesión
        return render(request, 'registration/loginColaborador.html', {'error': error})
    
    def post(self, request):
        correo = request.POST.get('correo')
        contrasenia = request.POST.get('contrasenia')
        user = authenticate(username=correo, password=contrasenia)
        if user is not None:
            login(request, user)
            request.session['correoColaborador'] = correo
            request.session['contraseniaColaborador'] = contrasenia
            return redirect('InterfazColaborador')
        else:
            request.session['error'] = 'Credenciales incorrectas'
            return redirect('LoginColaborador')

class Colaborador(viewsets.ViewSet):
    @method_decorator(login_required)
    def interfaz_colaborador(self, request):
        if request.method == 'POST':
            codigo = request.POST.get('codigo')
            id_bloque = request.POST.get('id_bloque')
            id_congreso = request.POST.get('id_congreso')
            correoColaborador = request.session.get('correoColaborador')
            contraseniaColaborador = request.session.get('contraseniaColaborador')
            try:
                colaborador = MaeColaborador.objects.get(correo=correoColaborador, contrasenia=contraseniaColaborador)
                if not TrsAsistencia.objects.filter(codparticipante=codigo, idbloque=id_bloque).exists():
                    nueva_asistencia = TrsAsistencia(
                        idcongreso_id=id_congreso,
                        codparticipante_id=codigo,
                        idbloque_id=id_bloque,
                    )
                    nueva_asistencia.save()    
                    mensaje = "Registro exitoso"
                else:
                    mensaje = "El código de participante ya se encuentra registrado en este bloque"
            except Exception:
                mensaje = 'Error al guardar la asistencia'
            return redirect('InterfazColaborador')
        else:
            correoColaborador = request.session.get('correoColaborador')
            contraseniaColaborador = request.session.get('contraseniaColaborador')
            colaborador = MaeColaborador.objects.get(correo=correoColaborador, contrasenia=contraseniaColaborador)
            dia_actual = date.today()
            dia_actual = dia_actual.strftime('%d/%m/%Y')
            bloques = MaeBloque.objects.filter(idcongreso=colaborador.idcongreso)
            return render(request, 'asistencia_colaborador.html', {
                'colaborador': colaborador, 
                'bloques': bloques, 
                'congreso': colaborador.idcongreso,
                'dia_actual': dia_actual
            })