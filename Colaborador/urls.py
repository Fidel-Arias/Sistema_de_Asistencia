from django.urls import path, include
from .views import Colaborador

urlpatterns = [
    path('registrar_asistencias/<str:correo>/<str:pk>', Colaborador.as_view({'get':'ingresoColaborador'}), name='Colaborador'),
    path('registrar_asistencia/', Colaborador.as_view({'post': 'registrar_asistencia'}), name='registrar_asistencia'),
]