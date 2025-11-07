from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import UsuarioPersonalizado
from .forms import RegistroForm
from proyectos.models import Proyecto
from tareas.models import Tarea
from django.utils import timezone

class RegistroView(CreateView):
    model = UsuarioPersonalizado
    form_class = RegistroForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return response

@login_required
def dashboard(request):
    usuario = request.user
    
    # Proyectos donde el usuario es creador o miembro
    proyectos = Proyecto.objects.filter(
        Q(miembros=usuario) | Q(creador=usuario)
    ).distinct().order_by('-fecha_creacion')[:5]
    
    # Tareas asignadas al usuario
    tareas_asignadas = Tarea.objects.filter(
        Q(asignado_a=usuario) & 
        Q(estado__in=['pendiente', 'en_progreso'])
    ).order_by('prioridad', 'fecha_vencimiento')[:10]
    
    # Estadísticas
    total_proyectos = Proyecto.objects.filter(
        Q(miembros=usuario) | Q(creador=usuario)
    ).distinct().count()
    
    tareas_pendientes = Tarea.objects.filter(
        asignado_a=usuario, 
        estado__in=['pendiente', 'en_progreso']
    ).count()
    
    tareas_vencidas = Tarea.objects.filter(
        asignado_a=usuario,
        estado__in=['pendiente', 'en_progreso'],
        fecha_vencimiento__lt=timezone.now().date()
    ).count()
    
    context = {
        'proyectos': proyectos,
        'tareas_asignadas': tareas_asignadas,
        'total_proyectos': total_proyectos,
        'tareas_pendientes': tareas_pendientes,
        'tareas_vencidas': tareas_vencidas,
    }
    return render(request, 'dashboard.html', context)

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')