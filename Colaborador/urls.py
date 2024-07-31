from django.urls import path
from .views import Colaborador

urlpatterns = [
    path('interfaz_colaborador/', Colaborador.as_view({'get':'interfaz_colaborador', 'post': 'interfaz_colaborador'}), name='InterfazColaborador'),
]
