#!/usr/bin/env python3
"""
Script de inicio para producción - Sistema Piscícola
"""
import os
import sys
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def init_production():
    """Inicializar aplicación para producción"""
    try:
        # Importar y configurar la aplicación
        from app import app
        from database_config import init_db
        
        # Configurar para producción
        os.environ['FLASK_ENV'] = 'production'
        
        # Inicializar base de datos
        with app.app_context():
            init_db()
            logging.info("✅ Base de datos inicializada correctamente")
        
        logging.info("🚀 Sistema Piscícola listo para producción")
        return app
        
    except Exception as e:
        logging.error(f"❌ Error en inicialización: {e}")
        sys.exit(1)

if __name__ == '__main__':
    app = init_production()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
