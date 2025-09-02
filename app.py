
from flask import Flask
from config import Config
from routes import bp as routes_bp
import os

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    # Configuración para desarrollo local
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))  # Render usa PORT en lugar de FLASK_PORT
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🌐 Servidor iniciando en http://{host}:{port}")
    print(f"🔗 Acceso local: http://localhost:{port}")
    print(f"🌍 Acceso en red: http://[IP-de-este-PC]:{port}")
    print("📋 Usuario: admin | Contraseña: admin123")
    
    app.run(host=host, port=port, debug=debug, threaded=True)
