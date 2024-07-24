from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import viewsets
from Admin.models import MaeAdministrador
from Participantes.models import MaeParticipantes
from Colaborador.models import MaeColaborador

# Create your views here.

class LoginView(viewsets.ViewSet):
    def login_user(self, request):
        if request.session.get('correo_admin') and request.session.get('contrasenia_admin'):
            del request.session['correo_admin']
            del request.session['contrasenia_admin']
        return render(request, 'login.html')
    
    def login_colaborador(self, request):
        return render(request, 'loginColaborador.html')
    
    def login_admin(self, request):
        return render(request, 'loginAdmin.html')
