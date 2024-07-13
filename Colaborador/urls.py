from django.urls import path
from .views import Colaborador

urlpatterns = [
    path('registrar_asistencia/', Colaborador.as_view({'post': 'registrar_asistencia'}), name='registrar_asistencia'),
    path('ingreso_colaborador/', Colaborador.as_view({'post': 'ingresoColaborador'}), name='ingreso_colaborador'),
]
