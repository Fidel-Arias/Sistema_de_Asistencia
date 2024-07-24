from django import forms
from .models import MaeColaborador

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = MaeColaborador
        fields = ('idcolaborador', 'nombre', 'apellido', 'correo', 'contrasenia', 'idtipo', 'idcongreso')