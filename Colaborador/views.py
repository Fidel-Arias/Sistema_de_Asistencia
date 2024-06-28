from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ColaboradorSerializer
from .models import MaeColaborador
from Bloque.models import MaeBloque
from CongresoJINIS.models import MaeCongresoJinis
from Asistencia.models import TrsAsistencia

from Bloque.models import MaeBloque
from CongresoJINIS.models import MaeCongresoJinis

class Colaborador(viewsets.ViewSet):
    queryset = MaeColaborador.objects.all()
    serializer_class = ColaboradorSerializer

    def ingresoColaborador(self, request, correo, pk):
        try:
            colaborador = MaeColaborador.objects.get(contrasenia=pk)
        except MaeColaborador.DoesNotExist:
            print("No existe chavo")
            return render(request, 'loginColaborador.html', {'current_page': 'error_admin'})
        colaborador_data = ColaboradorSerializer(colaborador)
        print('probando:', colaborador_data['nombre'].value)
        bloques_data = MaeBloque.objects.all()
        congreso_data = MaeCongresoJinis.objects.all()
        return render(request, 'colaborador.html', {'colaborador_data': colaborador_data.data, 'bloques_data': bloques_data, 'congreso_data': congreso_data})

    def registrar_asistencia(self, request):
        if request.method == "POST":
            codigo = request.POST.get('codigo')
            id_bloque = request.POST.get('id_bloque')
            id_congreso = request.POST.get('id_congreso')
            # print('ID BLOQUE: ', id_bloque)
            if not codigo:
                return JsonResponse({'success': False, 'message': 'Código no proporcionado'}, status=400)
            
            try:
                nueva_asistencia = TrsAsistencia(
                    idcongreso_id=id_congreso,
                    codparticipante_id=codigo,
                    idbloque_id=id_bloque,
                )
                nueva_asistencia.save()
                
                mensaje = "Registro exitoso"
                bloques_data = MaeBloque.objects.all()
                congreso_data = MaeCongresoJinis.objects.all()
                return render(request, 'colaborador.html', {'colaborador': None, 'mensaje': mensaje, 'bloques_data': bloques_data, 'congreso_data': congreso_data})
            
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)}, status=500)
            
        
        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)