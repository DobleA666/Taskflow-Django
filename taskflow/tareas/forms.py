from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Escribe tu comentario aquí...'
            }),
        }
        labels = {
            'contenido': 'Nuevo Comentario'
        }