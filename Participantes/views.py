from rest_framework import viewsets, response, status
from django.shortcuts import render, get_list_or_404, redirect
from .models import MaeParticipantes
from .serializers import ParticipanteSerializer

# Create your views here.

class viewParticipantes(viewsets.ModelViewSet):
    queryset = MaeParticipantes.objects.all()
    serializer_class = ParticipanteSerializer

    def list(self, request):
        # Retorna una respuesta vacía o personalizada
        return response.Response({"detail": "Esta ruta no está disponible."}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        try:
            participante = MaeParticipantes.objects.get(pk=pk)
        except MaeParticipantes.DoesNotExist:
            return response.Response({'detail': 'No existe este participante'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ParticipanteSerializer(participante)
        print('Requested codigo User: ', request.session.get('codparticipante'))
        print('probando:', serializer['email'].value)
        return render(request, 'participante.html', {'participante_data': serializer.data})




    
    
