from django.urls import path
from .views import viewParticipantes


urlpatterns = [
    path('user/', viewParticipantes.as_view({'get': 'participant'})),
    path('user/<str:pk>', viewParticipantes.as_view({'get': 'retrieve'}), name="Participante"),
]