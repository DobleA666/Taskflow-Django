from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaTareas.as_view(), name='lista_tareas'),
    path('<int:pk>/', views.DetalleTarea.as_view(), name='detalle_tarea'),
    path('<int:pk>/editar/', views.ActualizarTarea.as_view(), name='actualizar_tarea'),
    path('<int:pk>/eliminar/', views.EliminarTarea.as_view(), name='eliminar_tarea'),
    
    # URLs para comentarios
    path('<int:tarea_id>/comentario/crear/', views.CrearComentario.as_view(), name='crear_comentario'),
    path('comentario/<int:pk>/eliminar/', views.EliminarComentario.as_view(), name='eliminar_comentario'),
]