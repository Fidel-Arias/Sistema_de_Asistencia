from django.urls import path
from .views import adminView, ingresoAdmin

urlpatterns = [
    path('', adminView.as_view({'get':'index'}), name='InterfazAdministrador'),
    path('bienvenido/', ingresoAdmin, name='Administrador'),
    path('generar_reporte/', adminView.as_view({'get':'generar_reporte'}), name='GenerarReporte'),
    path('registrar_colaboradores/', adminView.as_view({'get':'registrar_colaboradores'}), name='RegistrarColaboradores'),
    path('registrar_ponencias/', adminView.as_view({'get':'registrar_ponencia'}), name='RegistrarPonencia'),
    path('registrar_ponentes/', adminView.as_view({'get':'registrar_ponentes'}), name='RegistrarPonentes'),
    path('registrar_universidades/', adminView.as_view({'get':'registrar_universidades'}), name='RegistrarUniversidades'),
    path('registrar_bloques/', adminView.as_view({'get':'registrar_bloques'}), name='RegistrarBloques'),
]