from django.urls import path, include
from .views import Colaborador

urlpatterns = [
    path('registrar_asistencias/', Colaborador.as_view({'get':''}), name='RegistroAsistencia'),
]