from django.shortcuts import render, redirect
from .decorators import participante_login_required
from django.urls import reverse
from django.views import View
from .models import MaeParticipantes
from Asistencia.models import TrsAsistencia
from ParticipanteCongreso.models import ParticipanteCongreso
from rest_framework import viewsets
from django.utils.decorators import method_decorator

class LoginView(View):
    def get(self, request):
        error = request.session.pop('error', None)  # Obtiene y elimina el mensaje de error de la sesión
        return render(request, 'login/login.html', {'error': error})  # Renderiza el formulario de login

    def post(self, request):
        codparticipante = request.POST.get('codigo')
        print(codparticipante)

        if not codparticipante:
            request.session['error'] = 'Debes ingresar un código'
            return redirect('Login')

        try:
            participante = MaeParticipantes.objects.get(pk=codparticipante)
            print('si ingrese')
            request.session['codparticipante'] = participante.pk  # Se guarda el código de participante en la sesión
            print('redirige')
            return redirect(reverse('Participante', kwargs={'pk':participante.pk}))  # Redirige a la página de Participante después del inicio de sesión exitoso
        except MaeParticipantes.DoesNotExist:
            request.session['error'] = 'Credenciales incorrectas'
            return redirect('Login')  # Redirige al formulario de login


class viewParticipantes(viewsets.ViewSet):
    @method_decorator(participante_login_required)
    def interfaz_user(self, request, pk):
        codparticipante = request.session.get('codparticipante')
        if codparticipante != str(pk):
            request.session['error'] = 'Acceso inválido'
            return redirect('Login')  # Redirigir si no está autenticado o si intenta acceder a otro usuario

        participante = MaeParticipantes.objects.get(pk=pk)
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
    
    @method_decorator(participante_login_required)
    def cerrar_sesion(self, request):
        request.session.flush()
        return redirect('Login')  # Redirige al formulario de login






    
    
