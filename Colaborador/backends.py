from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import MaeColaborador

class ColaboradorAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            colaborador = MaeColaborador.objects.get(correo=username)
            if colaborador.contrasenia == password:
                user, created = User.objects.get_or_create(username=username)
                return user
            else:
                return None
        except MaeColaborador.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None