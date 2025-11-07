from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaProyectos.as_view(), name='lista_proyectos'),
    path('crear/', views.CrearProyecto.as_view(), name='crear_proyecto'),
    path('<int:pk>/', views.DetalleProyecto.as_view(), name='detalle_proyecto'),
    path('<int:pk>/editar/', views.ActualizarProyecto.as_view(), name='actualizar_proyecto'),
    path('<int:pk>/eliminar/', views.EliminarProyecto.as_view(), name='eliminar_proyecto'),
    path('<int:proyecto_id>/tarea/crear/', views.CrearTareaProyecto.as_view(), name='crear_tarea_proyecto'),
]