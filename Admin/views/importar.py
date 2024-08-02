from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from Congreso.models import MaeCongreso
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from Participantes.models import MaeParticipantes
from tipoDocumento.models import MaeTipodocumento
from tipoParticipante.models import MaeTipoParticipante
from ParticipanteCongreso.models import ParticipanteCongreso
from django.db import transaction
from django.contrib import messages
import qrcode
import json
import pandas as pd

#Variables locales
archivo_subido = False

class Importar_Datos(viewsets.ViewSet):
    @method_decorator(login_required)
    def importar_datos(self, request):
        #Quitar el idcongreso de participantes es redundadnte y con la trs_ASistencia se puede verificar asi mismo quitar el diseño del html implementado
        global archivo_subido
        if request.method == 'POST' and request.FILES['file']:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)
            idcongreso = request.POST.get('congreso')

            #Procesando el archivo
            try:
                if filename.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                elif filename.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    messages.error(request, 'Formato de archivo no soportado')
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {e}')

            datos_participante = []
            for index, row in df.iterrows():
                datos_participante.append({
                    'DNI': row['DNI'],
                    'AP_PATERNO': row['Ap. Paterno'],
                    'AP_MATERNO': row['Ap. Materno'],
                    'NOMBRES': row['Nombres'],
                    'CORREO': row['Correo'],
                    'TIPO': row['Tipo'].upper(),
                })

            for dato in datos_participante:
                agregando_participantes = MaeParticipantes(
                    codparticipante=dato['DNI'],
                    ap_paterno=dato['AP_PATERNO'],
                    ap_materno=dato['AP_MATERNO'],
                    nombre=dato['NOMBRES'],
                    correo=dato['CORREO'],
                    idtipodoc=MaeTipodocumento.objects.get(pk=1),
                    idtipo=MaeTipoParticipante.objects.get(dstipo=dato['TIPO'])
                )
                agregando_participantes.save()
            archivo_subido = True
            fs.delete(filename)

            #Asociando a la tabla ParticipanteCongreso
            participantes = MaeParticipantes.objects.all()
            with transaction.atomic():
                for participante in participantes:
                    ParticipanteCongreso.objects.create(
                        codparticipante=MaeParticipantes.objects.get(pk=participante.pk),
                        idcongreso=MaeCongreso.objects.get(pk=idcongreso)
                    )

            messages.success(request, 'Archivo importado y procesado con éxito')
            return redirect('ImportarDatos')
        else:
            congresos = MaeCongreso.objects.all().order_by('pk')
            return render(request, 'pages/importarDatos.html', {
                'current_page': 'importar_datos',
                'congresos':congresos,
                'archivo_subido': archivo_subido
            })
        
class Generar_QRCode(viewsets.ViewSet):
    @method_decorator(login_required)
    def generar_codigo_qrcode(self, request):
        global archivo_subido
        if request.method == 'POST':
            participantes_congreso = ParticipanteCongreso.objects.all()
            data = {}
            for participante_congreso in participantes_congreso:
                participante = participante_congreso.codparticipante
                congreso = participante_congreso.idcongreso
                data = {
                    'DNI': participante.codparticipante,
                    'AP_PATERNO': participante.ap_paterno,
                    'AP_MATERNO': participante.ap_materno,
                    'NOMBRES': participante.nombre,
                    'CORREO': participante.correo,
                    'CONGRESO': congreso.idcongreso
                }
                json_data = json.dumps(data)
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(json_data)
                qr.make(fit=True)
                img = qr.make_image(fill_color='black', back_color='white')

                #save img
                file_path = f"static/qrcodes/{participante.pk}.png"
                #Se guarda la url de la carpeta de su codigo qr del participante
                participante.qr_code = file_path
                participante.save()
                img.save(file_path)
                file_path
            
            messages.success(request, 'Códigos QR generado con éxito')
            congresos = MaeCongreso.objects.all().order_by('pk')
            archivo_subido = False
            return render(request, 'pages/importarDatos.html', {
                'current_page': 'importar_datos',
                'congresos':congresos,
                'archivo_subido': archivo_subido
            })
        else:
            return redirect('ImportarDatos')
    

#Posible url: https://sistemaasistenciajinis.com