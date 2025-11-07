from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from .models import Tarea, Comentario
from proyectos.forms import TareaForm
from .forms import ComentarioForm  # ¡Falta este import!

class ListaTareas(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = 'tareas/lista_tareas.html'
    context_object_name = 'tareas'
    paginate_by = 8
    
    def get_queryset(self):
        queryset = Tarea.objects.filter(
            Q(proyecto__miembros=self.request.user) | 
            Q(asignado_a=self.request.user) |
            Q(creador=self.request.user)
        ).distinct().order_by('prioridad', '-fecha_creacion')
        
        # Filtros
        estado_filter = self.request.GET.get('estado', '')
        prioridad_filter = self.request.GET.get('prioridad', '')
        
        if estado_filter:
            queryset = queryset.filter(estado=estado_filter)
        if prioridad_filter:
            queryset = queryset.filter(prioridad=prioridad_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estado_filter'] = self.request.GET.get('estado', '')
        context['prioridad_filter'] = self.request.GET.get('prioridad', '')
        return context

class DetalleTarea(LoginRequiredMixin, DetailView):
    model = Tarea
    template_name = 'tareas/detalle_tarea.html'
    context_object_name = 'tarea'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentario_form'] = ComentarioForm()
        context['comentarios'] = self.object.comentarios.all().order_by('-fecha_creacion')
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ComentarioForm(request.POST)
        
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.tarea = self.object
            comentario.autor = request.user
            comentario.save()
            
            messages.success(request, 'Comentario agregado exitosamente!')
            return redirect('detalle_tarea', pk=self.object.pk)
        else:
            # Si el formulario no es válido, recargar la página con errores
            context = self.get_context_data()
            context['comentario_form'] = form
            return self.render_to_response(context)

class CrearComentario(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'tareas/agregar_comentario.html'
    
    def form_valid(self, form):
        tarea = get_object_or_404(Tarea, pk=self.kwargs['tarea_id'])
        form.instance.tarea = tarea
        form.instance.autor = self.request.user
        messages.success(self.request, 'Comentario agregado exitosamente!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('detalle_tarea', kwargs={'pk': self.kwargs['tarea_id']})
    
class ComentarioPermisoMixin:
    def dispatch(self, request, *args, **kwargs):
        comentario = self.get_object()
        # Permitir si: es el autor del comentario, creador de la tarea, o creador del proyecto
        if (request.user == comentario.autor or 
            request.user == comentario.tarea.creador or 
            request.user == comentario.tarea.proyecto.creador):
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'No tienes permisos para realizar esta acción.')
            return redirect('detalle_tarea', pk=comentario.tarea.pk)

class EliminarComentario(LoginRequiredMixin, ComentarioPermisoMixin, DeleteView):
    model = Comentario
    template_name = 'tareas/eliminar_comentario.html'
    context_object_name = 'comentario'
    
    def get_success_url(self):
        messages.success(self.request, 'Comentario eliminado exitosamente!')
        return reverse_lazy('detalle_tarea', kwargs={'pk': self.object.tarea.pk})

class ActualizarTarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tareas/actualizar_tarea.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pasar el proyecto_id para filtrar usuarios asignables
        kwargs['proyecto_id'] = self.object.proyecto.id
        return kwargs
    
    def form_valid(self, form):
        # Si la tarea se marca como completada, establecer fecha_completado
        if form.cleaned_data['estado'] == 'completada' and not self.object.fecha_completado:
            form.instance.fecha_completado = timezone.now()
        elif form.cleaned_data['estado'] != 'completada':
            form.instance.fecha_completado = None
            
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('detalle_tarea', kwargs={'pk': self.object.pk})

class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    template_name = 'tareas/eliminar_tarea.html'
    success_url = reverse_lazy('lista_tareas')