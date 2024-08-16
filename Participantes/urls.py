from django.urls import path, include
from .views import viewParticipantes

urlpatterns = [
    path('<int:pk>/', viewParticipantes.as_view({'get':'interfaz_user'}), name="Participante"),  # URL para la vista del participante
    path('cerrar_Sesion/', viewParticipantes.as_view({'get':'cerrar_sesion'}), name="Salir"),
    path('', include('Ponencia.urls')),
]