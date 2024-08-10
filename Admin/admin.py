from django.views import View
from django.http import JsonResponse
from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
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
        admin = authenticate(username=correo, password=contrasenia)
        if admin is not None:
            login(request, admin)
            request.session['correo_admin'] = correo
            request.session['contrasenia_admin'] = contrasenia
            return redirect('InterfazAdministrador')
        else:
            request.session['error'] = 'Usuario o contraseña incorrectos'
            return redirect('LoginAdmin')
        
class RegisterAdmin(View):
    def get(self, request):
        return render(request, 'register/register_admin.html')
    
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            data = json.loads(request.body)
            formulario_data = data.get('formulario')
            print(formulario_data)
            # Aquí puedes realizar cualquier operación con `formulario_data`
            return JsonResponse({
                'status': 'success',
            })
        except json.JSONDecodeError:
            return redirect('RegisterAdmin')


class Cerrar_Sesion(viewsets.ViewSet):
    def cerrar_sesion(self, request):
        del request.session['correo_admin']
        del request.session['contrasenia_admin']
        return redirect('LoginAdmin')