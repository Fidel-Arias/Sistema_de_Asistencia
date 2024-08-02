from django import forms
from .models import MaeAdministrador

class AdministradorForm(forms.ModelForm):
    class Meta:
        model = MaeAdministrador
        fields = ('idadministrador', 'nombres', 'apellidos', 'correo', 'contrasenia', 'idtipo', 'idcongreso')