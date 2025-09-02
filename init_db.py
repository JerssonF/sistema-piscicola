#!/usr/bin/env python3
"""
Script para inicializar la base de datos en producción
"""
from app import app
from database_config import init_db

def initialize_database():
    """Inicializa la base de datos con las tablas necesarias"""
    with app.app_context():
        try:
            init_db()
            print("✅ Base de datos inicializada correctamente")
        except Exception as e:
            print(f"❌ Error al inicializar la base de datos: {e}")

if __name__ == "__main__":
    initialize_database()
