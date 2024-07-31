from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import MaeAdministrador

class AdminAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            admin = MaeAdministrador.objects.get(correo=username)
            if admin.contrasenia == password:
                user, created = User.objects.get_or_create(username=username)
                return user
            else:
                return None
        except MaeAdministrador.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None