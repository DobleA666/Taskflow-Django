from django import forms
from .models import Proyecto
from tareas.models import Tarea

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_vencimiento', 'miembros']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'miembros': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = 'Nombre del Proyecto'
        self.fields['descripcion'].label = 'Descripción del Proyecto'
        self.fields['fecha_vencimiento'].label = 'Fecha Límite'
        self.fields['miembros'].label = 'Colaboradores'

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'estado', 'prioridad', 'fecha_vencimiento', 'asignado_a']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el título de la tarea'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'asignado_a': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        proyecto_id = kwargs.pop('proyecto_id', None)
        super().__init__(*args, **kwargs)
        
        # Mejorar labels y agregar placeholders
        self.fields['titulo'].label = 'Título de la Tarea'
        self.fields['descripcion'].label = 'Descripción Detallada'
        self.fields['fecha_vencimiento'].label = 'Fecha Límite'
        self.fields['asignado_a'].label = 'Asignar a'
        self.fields['prioridad'].label = 'Nivel de Prioridad'
        self.fields['estado'].label = 'Estado Actual'
        
        # Hacer campos requeridos
        self.fields['titulo'].required = True
        self.fields['estado'].required = True
        self.fields['prioridad'].required = True
        
        # Filtrar usuarios asignables por proyecto
        if proyecto_id:
            from proyectos.models import Proyecto
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
                miembros = proyecto.miembros.all()
                if miembros:
                    self.fields['asignado_a'].queryset = miembros
                    self.fields['asignado_a'].empty_label = "Selecciona un miembro"
                else:
                    self.fields['asignado_a'].queryset = proyecto.miembros.none()
                    self.fields['asignado_a'].help_text = 'No hay miembros en este proyecto. Agrega miembros primero.'
            except Proyecto.DoesNotExist:
                pass
    
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if titulo and len(titulo.strip()) < 3:
            raise forms.ValidationError("El título debe tener al menos 3 caracteres.")
        return titulo.strip()
    
    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        if fecha_vencimiento:
            from django.utils import timezone
            if fecha_vencimiento < timezone.now().date():
                raise forms.ValidationError("La fecha de vencimiento no puede ser en el pasado.")
        return fecha_vencimiento