from django import forms
from .models import Comunicado

class ComunicadoForm(forms.ModelForm):
    class Meta:
        model = Comunicado
        fields = ['titulo', 'contenido', 'tipo_comunicado']

class AsistenciaForm(forms.Form):
    asistencia = forms.BooleanField(required=False)
