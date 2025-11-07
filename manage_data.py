# Script para crear datos de prueba
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskflow.settings')
django.setup()

from django.contrib.auth import get_user_model
from proyectos.models import Proyecto
from tareas.models import Tarea
from datetime import date, timedelta

Usuario = get_user_model()

# Crear usuarios de prueba
def crear_usuarios():
    admin_user = Usuario.objects.create_superuser(
        username='admin',
        email='admin@taskflow.com',
        password='admin123',
        rol='admin'
    )
    
    usuario1 = Usuario.objects.create_user(
        username='maria',
        email='maria@taskflow.com',
        password='test123',
        rol='miembro',
        first_name='María',
        last_name='García'
    )
    
    usuario2 = Usuario.objects.create_user(
        username='carlos',
        email='carlos@taskflow.com',
        password='test123', 
        rol='miembro',
        first_name='Carlos',
        last_name='López'
    )
    
    return admin_user, usuario1, usuario2

def crear_proyectos_y_tareas():
    admin_user, maria, carlos = crear_usuarios()
    
    # Proyecto 1
    proyecto1 = Proyecto.objects.create(
        nombre='Desarrollo Web TaskFlow',
        descripcion='Desarrollo del sistema de gestión de proyectos TaskFlow',
        fecha_vencimiento=date.today() + timedelta(days=30),
        creador=admin_user
    )
    proyecto1.miembros.add(maria, carlos)
    
    # Tareas para proyecto 1
    tarea1 = Tarea.objects.create(
        titulo='Diseñar modelos de base de datos',
        descripcion='Crear los modelos User, Project, Task, Comment',
        proyecto=proyecto1,
        asignado_a=maria,
        creador=admin_user,
        prioridad=3,
        fecha_vencimiento=date.today() + timedelta(days=5)
    )
    
    tarea2 = Tarea.objects.create(
        titulo='Implementar autenticación',
        descripcion='Sistema de login, registro y permisos',
        proyecto=proyecto1,
        asignado_a=carlos,
        creador=admin_user,
        prioridad=3,
        fecha_vencimiento=date.today() + timedelta(days=7)
    )
    
    print("✅ Datos de prueba creados exitosamente!")
    print(f"👤 Usuarios: admin/admin123, maria/test123, carlos/test123")
    print(f"📁 Proyecto: {proyecto1.nombre}")
    print(f"📋 Tareas: {tarea1.titulo}, {tarea2.titulo}")

if __name__ == '__main__':
    crear_proyectos_y_tareas()