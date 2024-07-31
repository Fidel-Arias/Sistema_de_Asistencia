from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import MaeParticipantes

class CodParticipanteAuthBackend (BaseBackend):
    def authenticate(self, request, username=None):
        try:
            participante = MaeParticipantes.objects.get(codparticipante=username)
            user, created = User.objects.get_or_create(username=participante.codparticipante)
            return user
        except MaeParticipantes.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None