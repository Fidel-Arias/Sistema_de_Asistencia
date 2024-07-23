from django.urls import path
from .views import adminView, ingresoAdmin

urlpatterns = [
    path('bienvenido/', ingresoAdmin, name='Administrador'),
    path('generar_reporte/', adminView.as_view({'get':'generar_reporte'}), name='GenerarReporte'),
    path('registrar_colaboradores/', adminView.as_view({'get':'registrar_colaboradores', 'post':'registrar_colaboradores'}), name='RegistrarColaboradores'),
    path('registrar_ponencias/', adminView.as_view({'get':'registrar_ponencia', 'post':'registrar_ponencia'}), name='RegistrarPonencia'),
    path('registrar_ponentes/', adminView.as_view({'get':'registrar_ponentes', 'post':'registrar_ponentes'}), name='RegistrarPonentes'),
    path('registrar_congreso/', adminView.as_view({'get':'registrar_congreso', 'post':'registrar_congreso'}), name='RegistrarCongreso'),
    path('registrar_ubicacion/', adminView.as_view({'get':'registrar_ubicacion', 'post':'registrar_ubicacion'}), name='RegistrarUbicaciones'),
    path('registrar_bloques/', adminView.as_view({'get':'registrar_bloques', 'post':'registrar_bloques'}), name='RegistrarBloques'),
]