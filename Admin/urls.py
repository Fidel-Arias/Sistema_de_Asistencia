from django.urls import path
from .login_admin import Cerrar_Sesion
from .views import colaboradores, congreso, ponentes, bloques, ponencias, ubicacion, bloquesColaborador, reporte, importar, interfaz

urlpatterns = [
    path('bienvenido/', interfaz.Interfaz_Administrador.as_view({'get':'interfaz_administrador'}), name='InterfazAdministrador'),
    path('generar_reporte/', reporte.generar_reporte, name='GenerarReporte'),
    path('registrar_colaboradores/', colaboradores.Registrar_Colaboradores.as_view({'get':'registrar_colaboradores', 'post':'registrar_colaboradores'}), name='RegistrarColaboradores'),
    path('registrar_ponencias/', ponencias.Registrar_Ponencias.as_view({'get':'registrar_ponencias', 'post':'registrar_ponencias'}), name='RegistrarPonencia'),
    path('registrar_ponentes/', ponentes.Registrar_Ponentes.as_view({'get':'registrar_ponentes', 'post':'registrar_ponentes'}), name='RegistrarPonentes'),
    path('registrar_congreso/', congreso.Registrar_Congreso.as_view({'get':'registrar_congreso', 'post':'registrar_congreso'}), name='RegistrarCongreso'),
    path('registrar_ubicacion/', ubicacion.Registrar_Ubicacion.as_view({'get':'registrar_ubicacion', 'post':'registrar_ubicacion'}), name='RegistrarUbicaciones'),
    path('registrar_bloques/', bloques.Registrar_Bloques.as_view({'get':'registrar_bloques', 'post':'registrar_bloques'}), name='RegistrarBloques'),
    path('registrar_bloques_colaboradores/', bloquesColaborador.Registrar_Bloques_Colaborador.as_view({'get':'registrar_bloques_colaboradores', 'post':'registrar_bloques_colaboradores'}), name='RegistrarBloqueColaborador'),
    path('importar_datos/', importar.Importar_Datos.as_view({'get':'importar_datos', 'post':'importar_datos'}), name='ImportarDatos'),
    path('generar_qrcode/', importar.Generar_QRCode.as_view({'get':'generar_codigo_qrcode', 'post':'generar_codigo_qrcode'}), name='GenerarQRCode'),
    path('', Cerrar_Sesion.as_view({'get':'cerrar_sesion'}), name='CerrarSesion'),
]