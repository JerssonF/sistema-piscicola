# Sistema Piscícola - Configuración para Render

## Variables de entorno necesarias
PORT=5000
FLASK_ENV=production

## Comandos de construcción
pip install -r requirements.txt

## Comando de inicio
gunicorn --bind 0.0.0.0:$PORT --workers 1 app:app
