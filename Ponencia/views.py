from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from Participantes.decorators import participante_login_required
from Bloque.models import MaeBloque
from Participantes.models import MaeParticipantes

# Create your views here.
class viewPonencias(viewsets.ViewSet):
    @method_decorator(participante_login_required)
    def verPonencias(self, request, pk):
        codparticipante = request.session.get('codparticipante')
        if codparticipante != str(pk):
            request.session['error'] = 'Acceso inválido'
            return redirect('Login')  # Redirigir si no está autenticado o si intenta acceder a otro usuario
        
        bloques = MaeBloque.objects.filter().order_by('iddia__fecha')
        participante = MaeParticipantes.objects.get(pk=pk)
        return render(request, 'ponencias.html', {
            'ponencias': bloques,
            'participante': participante
        })
    