#!/bin/bash
# Script de inicio para producción en Render

echo "🚀 Iniciando Sistema Piscícola..."

# Verificar que Python está disponible
python --version

# Verificar que las dependencias están instaladas
pip list | grep -E "(Flask|gunicorn)"

# Inicializar la base de datos
echo "📁 Inicializando base de datos..."
python -c "
from app import app
from database_config import init_db
with app.app_context():
    init_db()
    print('Base de datos inicializada')
"

echo "✅ Configuración completa. Iniciando aplicación..."

# Iniciar con gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --log-level info app:app
