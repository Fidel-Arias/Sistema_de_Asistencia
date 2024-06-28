from django.urls import path
from .views import viewPonencias


urlpatterns = [
    path('ponencias/<str:codigoParticipante>', viewPonencias.as_view({'get':'verPonencias'}), name="Ponencias"),
]