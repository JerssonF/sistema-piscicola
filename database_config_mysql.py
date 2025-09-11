"""
🗄️ Configuración de Base de Datos MySQL para phpMyAdmin
"""

import mysql.connector
from mysql.connector import Error
import os

# Configuración de conexión MySQL
MYSQL_CONFIG = {
    'host': 'localhost',  # Cambia si tu servidor MySQL está en otro host
    'port': 3306,         # Puerto por defecto de MySQL
    'user': 'root',       # Usuario por defecto de XAMPP/WAMP
    'password': '',       # Contraseña (vacía por defecto en XAMPP)
    'database': 'piscicola',  # Nombre de la base de datos
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

def get_mysql_connection():
    """Obtiene una conexión a MySQL"""
    try:
        connection = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            database=MYSQL_CONFIG['database'],
            charset=MYSQL_CONFIG['charset']
        )
        return connection
    except Error as e:
        print(f"❌ Error conectando a MySQL: {e}")
        return None

def create_database():
    """Crea la base de datos si no existe"""
    try:
        # Conectar sin especificar base de datos
        connection = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            charset=MYSQL_CONFIG['charset']
        )
        
        cursor = connection.cursor()
        
        # Crear base de datos
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ Base de datos '{MYSQL_CONFIG['database']}' creada/verificada")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def init_mysql_tables():
    """Inicializa todas las tablas necesarias en MySQL"""
    connection = get_mysql_connection()
    if not connection:
        print("❌ No se pudo conectar a MySQL")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Tabla usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Tabla alimento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alimento (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque VARCHAR(50) NOT NULL,
                tipo_alimento VARCHAR(100) NOT NULL,
                cantidad_kg DECIMAL(10,2) NOT NULL,
                observaciones TEXT,
                frecuencia_toma VARCHAR(100),
                mortalidad INT DEFAULT 0,
                causa_mortalidad TEXT,
                acciones_correctivas TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Tabla muestreo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS muestreo (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque VARCHAR(50) NOT NULL,
                peso_promedio DECIMAL(10,2) NOT NULL,
                talla_promedio DECIMAL(10,2) NOT NULL,
                cantidad_peces INT NOT NULL,
                observaciones TEXT,
                frecuencia_toma VARCHAR(100),
                especie VARCHAR(100),
                biomasa DECIMAL(10,2),
                peces INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Tabla parametros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parametros (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque VARCHAR(50) NOT NULL,
                temperatura DECIMAL(5,2) NOT NULL,
                ph DECIMAL(4,2) NOT NULL,
                oxigeno DECIMAL(5,2) NOT NULL,
                amonio DECIMAL(5,2),
                nitrito DECIMAL(5,2),
                nitrato DECIMAL(5,2),
                observaciones TEXT,
                frecuencia_toma VARCHAR(100),
                oxigeno_disuelto DECIMAL(5,2),
                nitritos DECIMAL(5,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Tabla siembra
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS siembra (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque VARCHAR(50) NOT NULL,
                especie VARCHAR(100) NOT NULL,
                cantidad INT NOT NULL,
                peso_promedio DECIMAL(10,2) NOT NULL,
                proveedor VARCHAR(100),
                observaciones TEXT,
                destino VARCHAR(100),
                ovas_alevinos INT,
                hembras_machos VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Tabla ingreso_alimentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingreso_alimentos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                ingreso_comida VARCHAR(100) NOT NULL,
                cantidad DECIMAL(10,2) NOT NULL,
                transporte VARCHAR(100),
                observaciones TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Insertar usuario por defecto
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE username = %s', ('admin',))
        result = cursor.fetchone()
        if result[0] == 0:
            cursor.execute(
                'INSERT INTO usuarios (username, password) VALUES (%s, %s)',
                ('admin', 'admin123')
            )
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("✅ Todas las tablas MySQL creadas correctamente")
        return True
        
    except Error as e:
        print(f"❌ Error creando tablas: {e}")
        if connection.is_connected():
            connection.close()
        return False

def test_mysql_connection():
    """Prueba la conexión a MySQL"""
    try:
        connection = get_mysql_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 'Conexión MySQL exitosa' as status")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return True, result[0]
        else:
            return False, "No se pudo establecer la conexión"
    except Error as e:
        return False, str(e)

def get_mysql_info():
    """Obtiene información de la configuración MySQL"""
    return {
        'host': MYSQL_CONFIG['host'],
        'port': MYSQL_CONFIG['port'],
        'user': MYSQL_CONFIG['user'],
        'database': MYSQL_CONFIG['database'],
        'charset': MYSQL_CONFIG['charset']
    }

if __name__ == "__main__":
    print("🔧 CONFIGURACIÓN DE MYSQL PARA PHPMYADMIN")
    print("=" * 50)
    
    # Mostrar configuración
    config = get_mysql_info()
    print("📊 Configuración actual:")
    for key, value in config.items():
        if key == 'password':
            print(f"   {key}: {'*' * len(str(value)) if value else '(vacía)'}")
        else:
            print(f"   {key}: {value}")
    
    print("\n🔍 Probando conexión...")
    
    # Crear base de datos
    if create_database():
        # Probar conexión
        success, message = test_mysql_connection()
        if success:
            print(f"✅ {message}")
            
            # Crear tablas
            if init_mysql_tables():
                print("🎉 ¡Configuración MySQL completada!")
            else:
                print("❌ Error creando tablas")
        else:
            print(f"❌ Error de conexión: {message}")
    else:
        print("❌ No se pudo crear la base de datos")
