"""
🗄️ Configuración de Base de Datos SQLite para Producción
Compatible con Render.com y despliegue en la nube
"""

import sqlite3
import os
from pathlib import Path

def get_db_path():
    """Obtiene la ruta de la base de datos"""
    if os.environ.get('RENDER'):
        # En producción (Render), usar directorio temporal
        return '/tmp/piscicola.db'
    else:
        # En desarrollo local
        return os.path.join(os.path.dirname(__file__), 'piscicola.db')

def init_db():
    """Inicializa la base de datos con todas las tablas necesarias"""
    db_path = get_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla alimento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alimento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque TEXT NOT NULL,
                tipo_alimento TEXT NOT NULL,
                cantidad_kg REAL NOT NULL,
                observaciones TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla muestreo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS muestreo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque TEXT NOT NULL,
                peso_promedio REAL NOT NULL,
                talla_promedio REAL NOT NULL,
                cantidad_peces INTEGER NOT NULL,
                observaciones TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla parametros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parametros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque TEXT NOT NULL,
                temperatura REAL NOT NULL,
                ph REAL NOT NULL,
                oxigeno REAL NOT NULL,
                amonio REAL,
                nitrito REAL,
                nitrato REAL,
                observaciones TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla siembra
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS siembra (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque TEXT NOT NULL,
                especie TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                peso_promedio REAL NOT NULL,
                proveedor TEXT,
                observaciones TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar usuario por defecto si no existe
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE username = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                'INSERT INTO usuarios (username, password) VALUES (?, ?)',
                ('admin', 'admin123')
            )
        
        conn.commit()
        conn.close()
        
        print(f"✅ Base de datos inicializada correctamente en: {db_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return False

def get_connection():
    """Obtiene una conexión a la base de datos"""
    db_path = get_db_path()
    return sqlite3.connect(db_path)

def test_connection():
    """Prueba la conexión a la base de datos"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 'Conexión exitosa' as status")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return True, result[0]
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    print("🗄️ INICIALIZANDO BASE DE DATOS SQLITE")
    print("=====================================")
    
    # Inicializar base de datos
    if init_db():
        print("✅ Base de datos creada exitosamente")
        
        # Probar conexión
        success, message = test_connection()
        print(f"Prueba de conexión: {'✅ Exitosa' if success else '❌ Error'}")
        print(f"Mensaje: {message}")
    else:
        print("❌ Error creando la base de datos")
