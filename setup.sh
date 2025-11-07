#!/bin/bash

# Script de instalación para TaskFlow
echo "🚀 Configurando TaskFlow..."

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python -m venv venv

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar migraciones
echo "🗃️ Ejecutando migraciones..."
python manage.py migrate

# Crear superusuario
echo "👤 Creando superusuario..."
python manage.py createsuperuser

# Colectar archivos static
echo "🎨 Colectando archivos static..."
python manage.py collectstatic --noinput

echo "✅ ¡Configuración completada!"
echo "🎉 Para ejecutar el servidor: python manage.py runserver"
echo "📝 Accede a: http://127.0.0.1:8000/"