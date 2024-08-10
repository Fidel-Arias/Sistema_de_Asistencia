from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from .models import MaeParticipantes
from Asistencia.models import TrsAsistencia
from ParticipanteCongreso.models import ParticipanteCongreso
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginView(View):
    def get(self, request):
        error = request.session.pop('error', None)  # Obtiene y elimina el mensaje de error de la sesión
        return render(request, 'login/login.html', {'error': error})  # Renderiza el formulario de login

    def post(self, request):
        codparticipante = request.POST.get('codigo')
        user = authenticate(request, username=codparticipante)
        if user is not None:
            login(request, user)
            request.session['codigo'] = codparticipante
            return redirect('Participante')  # Redirige a la página de Participante después del inicio de sesión exitoso
        else:
            # Guarda el mensaje de error en la sesión
            request.session['error'] = 'Credenciales incorrectas'
            return redirect('Login')  # Redirige al formulario de login

class viewParticipantes(viewsets.ViewSet):
    @method_decorator(login_required)
    def interfaz_user(self, request):
        codigo = request.session.get('codigo')
        participante = MaeParticipantes.objects.get(pk=codigo)
        participante_congreso = ParticipanteCongreso.objects.get(codparticipante=participante.codparticipante)
        participante_qrcode_path = participante.qr_code.replace('static/', '')
        cantidad_asistencia = TrsAsistencia.objects.filter(idpc=participante_congreso).count()
        nombreParticipante = participante.nombre.split(' ')

        return render(request, 'participante.html', {
            'nombre': nombreParticipante[0].capitalize() + ' ' + participante.ap_paterno.capitalize() + ' ' + participante.ap_materno.capitalize(),
            'participante_data': participante,
            'participante_qrcode_path':participante_qrcode_path,
            'cantidad_asistencia':cantidad_asistencia
        })
    
    @method_decorator(login_required)
    def cerrar_sesion(self, request):
        request.session.clear()
        return redirect('Login')  # Redirige al formulario de login






    
    
