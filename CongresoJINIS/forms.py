from django import forms
from .models import MaeCongresoJinis

class CongresoJinisForm(forms.ModelForm):
    class Meta:
        model = MaeCongresoJinis
        fields = ['idcongreso', 'nombre', 'fechainicio', 'fechafin', 'asistenciatotal']