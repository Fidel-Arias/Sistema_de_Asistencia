from django.views import View
from django.http import JsonResponse
from .models import MaeAdministrador
from email_service.views import email_service
from rest_framework import viewsets
from django.urls import reverse
from django.shortcuts import render, redirect
from .decorators import administrador_login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

class LoginAdmin(View):
    def get(self, request):
        error = request.session.pop('error', None)  # Obtiene y elimina el mensaje de error de la sesión
        return render(request, 'login/loginAdmin.html', {'error': error})
    
    def post(self, request):
        correo = request.POST['correo']
        contrasenia = request.POST['contrasenia']
        try:
            administrador = MaeAdministrador.objects.get(correo=correo, contrasenia=contrasenia)
            request.session['codadministrador'] = administrador.pk
            return redirect(reverse('InterfazAdministrador', kwargs={'pk':administrador.pk}))
        except MaeAdministrador.DoesNotExist:
            request.session['error'] = 'Correo o contraseña incorrectos'
            return redirect('LoginAdmin')
        
class RegisterAdmin(View):
    def get(self, request):
        return render(request, 'register/register_admin.html')
    
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            data = json.loads(request.body)
            formulario_data = data.get('formulario')

            if not formulario_data:
                return JsonResponse({'status': 'error', 'message': 'Datos del formulario no proporcionados'})
            
            status_email = email_service(request, formulario_data)

            # enviar error de cuenta no existente
            if status_email == 'success':
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'Credenciales incorrectas'})
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failed', 'message': 'Error en la decodificación del JSON'})
        except Exception as e:
            print("Error encontrado: ", e)
            return JsonResponse({'status': 'failed', 'message': 'Ocurrió un error en el servidor'})


class Cerrar_Sesion(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def cerrar_sesion(self, request):
        request.session.flush()
        return redirect('LoginAdmin')
        