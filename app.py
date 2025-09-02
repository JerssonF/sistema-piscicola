
from flask import Flask
from config import Config
from routes import bp as routes_bp
import os

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(routes_bp)

# Inicializar base de datos si no existe
try:
    from database_config import init_db
    with app.app_context():
        init_db()
except Exception as e:
    pass  # En producción, fallar silenciosamente

if __name__ == '__main__':
    # Configuración para desarrollo local
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug, threaded=True)
