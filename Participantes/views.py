from rest_framework import viewsets, response, status
from django.urls import reverse
from django.shortcuts import render, get_list_or_404, redirect
from .models import MaeParticipantes
from .serializers import ParticipanteSerializer

# Create your views here.

class viewParticipantes(viewsets.ViewSet):
    queryset = MaeParticipantes.objects.all()
    serializer_class = ParticipanteSerializer

    def retrieve(self, request):
        if request.method == "POST":
            codigo = request.POST.get('codigo')
            request.session['codigo'] = codigo
            try:
                participante = MaeParticipantes.objects.get(pk=codigo)
                serializer = ParticipanteSerializer(participante)
                return render(request, 'participante.html', {'participante_data': serializer.data})
            except MaeParticipantes.DoesNotExist:
                return redirect(reverse('Login') + '?error=Usuario o contraseña incorrectos')
        else:
            codigo = request.session.get('codigo')
            participante = MaeParticipantes.objects.get(pk=codigo)
            serializer = ParticipanteSerializer(participante)
            return render(request, 'participante.html', {'participante_data':serializer.data})
    def exit(self, request):
        del request.session['codigo']
        return redirect('Login')




    
    
