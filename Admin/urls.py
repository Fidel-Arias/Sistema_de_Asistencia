from django.urls import path
from .login_admin import Cerrar_Sesion
from .views import congreso, cargosUsuario, ponentes, bloques, ponencias, ubicacion, bloquesColaborador, reporte, importar, interfaz

urlpatterns = [
    path('bienvenido/', interfaz.interfaz_administrador, name='InterfazAdministrador'),
    path('generar_reporte/', reporte.generar_reporte, name='GenerarReporte'),
    path('registrar_cargos_usuarios/', cargosUsuario.registrar_cargos_usuarios, name='RegistrarCargosUsuarios'),
    path('registrar_ponencias/', ponencias.registrar_ponencia, name='RegistrarPonencia'),
    path('registrar_ponentes/', ponentes.registrar_ponentes, name='RegistrarPonentes'),
    path('registrar_congreso/', congreso.registrar_congreso, name='RegistrarCongreso'),
    path('registrar_ubicacion/', ubicacion.registrar_ubicacion, name='RegistrarUbicaciones'),
    path('registrar_bloques/', bloques.registrar_bloques, name='RegistrarBloques'),
    path('registrar_bloques_colaboradores/', bloquesColaborador.registrar_bloques_colaboradores, name='RegistrarBloqueColaborador'),
    path('importar_datos/', importar.importar_datos, name='ImportarDatos'),
    path('generar_qrcode/', importar.generar_codigo_qrcode, name='GenerarQRCode'),
    path('', Cerrar_Sesion.as_view({'get':'cerrar_sesion'}), name='CerrarSesion'),
]