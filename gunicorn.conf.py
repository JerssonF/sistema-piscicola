"""
Configuración de Gunicorn para Render.com
"""

import os

# Configuración del servidor
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2

# Configuración de logs
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Configuración de la aplicación
preload_app = True
max_requests = 1000
max_requests_jitter = 100

# Configuración de reinicio
reload = False
reload_engine = "auto"

def when_ready(server):
    """Callback cuando el servidor está listo"""
    server.log.info("🚀 Sistema Piscícola iniciado correctamente")

def on_starting(server):
    """Callback al iniciar el servidor"""
    server.log.info("🔄 Iniciando Sistema Piscícola...")

def on_reload(server):
    """Callback al recargar"""
    server.log.info("🔄 Recargando Sistema Piscícola...")
