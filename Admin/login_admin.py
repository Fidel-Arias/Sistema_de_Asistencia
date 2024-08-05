from django.views import View
from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

class LoginAdmin(View):
    def get(self, request):
        error = request.session.pop('error', None)  # Obtiene y elimina el mensaje de error de la sesión
        return render(request, 'registration/loginAdmin.html', {'error': error})
    
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

class Cerrar_Sesion(viewsets.ViewSet):
    def cerrar_sesion(self, request):
        del request.session['correo_admin']
        del request.session['contrasenia_admin']
        return redirect('LoginAdmin')

    
    
    
        
    
    
    
    

