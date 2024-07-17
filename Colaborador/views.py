from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
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

    def ingresoColaborador(self, request):
        if request.method == "POST":
            correo = request.POST.get('correo')
            contrasenia = request.POST.get('contrasenia')
            try:
                colaborador = MaeColaborador.objects.get(correo=correo, contrasenia=contrasenia)
                request.session['correoColaborador'] = correo
                request.session['contraseniaColaborador'] = contrasenia
            except MaeColaborador.DoesNotExist:
                print("No existe")
                return redirect(reverse('LoguingColaborador') + '?error=Usuario-o-contraseña-incorrectos')

            colaborador_data = ColaboradorSerializer(colaborador)
            bloques_data = MaeBloque.objects.all()
            congreso_data = MaeCongresoJinis.objects.all()
            return render(request, 'colaborador.html', {
                'colaborador_data': colaborador_data.data, 
                'bloques_data': bloques_data, 
                'congreso_data': congreso_data, 
                'correo': correo, 
                'contrasenia': contrasenia
            })

    def registrar_asistencia(self, request):
        if request.method == "POST":
            codigo = request.POST.get('codigo')
            id_bloque = request.POST.get('id_bloque')
            id_congreso = request.POST.get('id_congreso')
            correoColaborador = request.session.get('correoColaborador')
            contraseniaColaborador = request.session.get('contraseniaColaborador')
            bloques_data = MaeBloque.objects.all()
            congreso_data = MaeCongresoJinis.objects.all()
            colaborador_data = None
            try:
                colaborador = MaeColaborador.objects.get(correo=correoColaborador, contrasenia=contraseniaColaborador)
                colaborador_data = ColaboradorSerializer(colaborador)
                if not TrsAsistencia.objects.filter(codparticipante=codigo, idbloque=id_bloque).exists():
                    nueva_asistencia = TrsAsistencia(
                        idcongreso_id=id_congreso,
                        codparticipante_id=codigo,
                        idbloque_id=id_bloque,
                    )
                    nueva_asistencia.save()    
                    mensaje = "Registro exitoso"
                else:
                    mensaje = "El código de participante ya se encuentra registrado en este bloque"
            except Exception:
                mensaje = 'Error al guardar la asistencia'
            return render(request, 'colaborador.html', {'colaborador_data': colaborador_data.data, 'mensaje': mensaje, 'bloques_data': bloques_data, 'congreso_data': congreso_data})
            
        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
