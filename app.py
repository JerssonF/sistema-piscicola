
from flask import Flask
from config import Config
from routes import bp as routes_bp
import os

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(routes_bp)

# Inicializar base de datos al inicio
try:
    from database_config import init_db
    with app.app_context():
        init_db()
        print("✅ Base de datos inicializada")
except Exception as e:
    print(f"❌ Error inicializando BD: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
