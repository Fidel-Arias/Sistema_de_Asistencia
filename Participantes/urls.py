from django.urls import path
from .views import viewParticipantes


urlpatterns = [
    path('perfil/', viewParticipantes.as_view({'get':'retrieve','post': 'retrieve'}), name="Participante"),
    path('', viewParticipantes.as_view({'get':'exit'}), name="Salir"),
]