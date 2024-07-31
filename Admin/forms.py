from django import forms
from .models import MaeAdministrador

class AdministradorForm(forms.ModelForm):
    class Meta:
        model = MaeAdministrador
        fields = ('idadministrador', 'nombre', 'apellido', 'correo', 'contrasenia', 'idtipo', 'idcongreso')