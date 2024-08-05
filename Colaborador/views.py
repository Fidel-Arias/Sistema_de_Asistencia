from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import MaeColaborador
from BloqueColaborador.models import BloqueColaborador
from Asistencia.models import TrsAsistencia
from ParticipanteCongreso.models import ParticipanteCongreso
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
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    @action(detail=False, methods=['post', 'get'])
    def interfaz_colaborador(self, request):
        if request.method == 'POST':
            try:
                data = request.data  # Usar request.data para obtener los datos JSON
                qr_data = json.loads(data.get('qr_code'))
                bloque_actual = json.loads(data.get('bloque'))
                
                participante = ParticipanteCongreso.objects.get(codparticipante=qr_data['DNI'], idcongreso=qr_data['CONGRESO'])
                bloque = BloqueColaborador.objects.get(idcongreso=qr_data['CONGRESO'], idbloque=bloque_actual)
                if not TrsAsistencia.objects.filter(idpc = participante, idbc = bloque).exists():
                    #Registro de asistencia
                    asistencia = TrsAsistencia(
                        idpc = participante,
                        idbc = bloque
                    )
                    asistencia.save()
                else:
                    print("El participante ya ha sido")

                # Simulación de procesamiento
                response_data = {
                    'status': 'success',
                    'message': f'Data recibida: {qr_data}'
                }
                return JsonResponse(response_data)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        else:
            correoColaborador = request.session.get('correoColaborador')
            contraseniaColaborador = request.session.get('contraseniaColaborador')
            colaborador = MaeColaborador.objects.get(correo=correoColaborador, contrasenia=contraseniaColaborador)
            colaborador_bloque = BloqueColaborador.objects.filter(idcolaborador=colaborador.idcolaborador)
            dia_actual = date.today().strftime('%d/%m/%Y')
            return render(request, 'asistencia_colaborador.html', {
                'colaborador': colaborador, 
                'bloques': colaborador_bloque, 
                'congreso': colaborador_bloque,
                'dia_actual': dia_actual
            })