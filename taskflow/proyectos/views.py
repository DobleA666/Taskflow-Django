from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Proyecto
from .forms import ProyectoForm, TareaForm
from tareas.models import Tarea
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# Mixin personalizado para verificar permisos de proyecto
class ProyectoPermisoMixin(UserPassesTestMixin):
    def test_func(self):
        proyecto = self.get_object()
        if hasattr(self, 'model') and self.model.__name__ == 'Proyecto':
            return self.request.user == proyecto.creador
        return self.request.user == proyecto.creador or self.request.user in proyecto.miembros.all()

class ListaProyectos(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyectos/lista_proyectos.html'
    context_object_name = 'proyectos'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Proyecto.objects.filter(
            Q(miembros=self.request.user) | Q(creador=self.request.user)
        ).distinct().order_by('-fecha_creacion')
        
        # Búsqueda avanzada
        search_query = self.request.GET.get('search', '')
        estado_filter = self.request.GET.get('estado', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query) | 
                Q(descripcion__icontains=search_query) |
                Q(creador__username__icontains=search_query)
            )
        
        if estado_filter:
            queryset = queryset.filter(estado=estado_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['estado_filter'] = self.request.GET.get('estado', '')
        return context

class DetalleProyecto(LoginRequiredMixin, ProyectoPermisoMixin, DetailView):
    model = Proyecto
    template_name = 'proyectos/detalle_proyecto.html'
    context_object_name = 'proyecto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = self.get_object()
        context['tareas'] = Tarea.objects.filter(proyecto=proyecto).order_by('prioridad', '-fecha_creacion')
        context['form_tarea'] = TareaForm(proyecto_id=proyecto.id)
        return context

class CrearProyecto(LoginRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/crear_proyecto.html'
    success_url = reverse_lazy('lista_proyectos')
    
    def form_valid(self, form):
        form.instance.creador = self.request.user
        return super().form_valid(form)

class ActualizarProyecto(LoginRequiredMixin, ProyectoPermisoMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/actualizar_proyecto.html'
    
    def get_success_url(self):
        return reverse_lazy('detalle_proyecto', kwargs={'pk': self.object.pk})

class EliminarProyecto(LoginRequiredMixin, ProyectoPermisoMixin, DeleteView):
    model = Proyecto
    template_name = 'proyectos/eliminar_proyecto.html'
    success_url = reverse_lazy('lista_proyectos')

class CrearTareaProyecto(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tareas/crear_tarea.html'
    success_message = "Tarea creada exitosamente!"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['proyecto_id'] = self.kwargs['proyecto_id']
        return kwargs
    
    def form_valid(self, form):
        proyecto = get_object_or_404(Proyecto, id=self.kwargs['proyecto_id'])
        form.instance.proyecto = proyecto
        form.instance.creador = self.request.user
        
        response = super().form_valid(form)
        messages.success(self.request, f'Tarea "{self.object.titulo}" creada exitosamente!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('detalle_proyecto', kwargs={'pk': self.kwargs['proyecto_id']})