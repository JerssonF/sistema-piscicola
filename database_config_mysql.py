"""
🗄️ Configuración de Base de Datos para Servidor en Red
Soporta conexiones locales y remotas
"""

import mysql.connector
import os
from mysql.connector import Error

class DatabaseConfig:
    """Configuración de base de datos con failover local/remoto"""
    
    # Configuración local (XAMPP)
    LOCAL_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '',
        'database': 'piscicola',
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }
    
    # Configuración remota
    REMOTE_CONFIG = {
        'host': os.environ.get('MYSQL_HOST', 'localhost'),
        'port': int(os.environ.get('MYSQL_PORT', 3306)),
        'user': os.environ.get('MYSQL_USER', 'piscicola_user'),
        'password': os.environ.get('MYSQL_PASSWORD', 'piscicola123'),
        'database': os.environ.get('MYSQL_DATABASE', 'piscicola'),
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }
    
    @staticmethod
    def get_connection():
        """
        Obtiene conexión a la base de datos con failover
        Intenta primero configuración local, luego remota
        """
        
        # Intentar conexión local primero
        try:
            print("🔄 Intentando conexión local a MySQL...")
            connection = mysql.connector.connect(**DatabaseConfig.LOCAL_CONFIG)
            if connection.is_connected():
                print("✅ Conexión local exitosa")
                return connection
        except Error as e:
            print(f"❌ Conexión local falló: {e}")
        
        # Intentar conexión remota
        try:
            print("🔄 Intentando conexión remota a MySQL...")
            connection = mysql.connector.connect(**DatabaseConfig.REMOTE_CONFIG)
            if connection.is_connected():
                print("✅ Conexión remota exitosa")
                return connection
        except Error as e:
            print(f"❌ Conexión remota falló: {e}")
        
        # Si ambas fallan
        raise Exception("❌ No se pudo conectar a MySQL (local ni remoto)")
    
    @staticmethod
    def test_connection():
        """Prueba la conexión a la base de datos"""
        try:
            conn = DatabaseConfig.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 'Conexión exitosa' as status")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return True, result[0]
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_server_info():
        """Obtiene información del servidor MySQL"""
        try:
            conn = DatabaseConfig.get_connection()
            info = {
                'server_version': conn.get_server_info(),
                'connection_id': conn.connection_id,
                'server_host': conn.server_host,
                'server_port': conn.server_port,
                'user': conn.user
            }
            conn.close()
            return info
        except Exception as e:
            return {'error': str(e)}

def verificar_tablas():
    """Verifica que todas las tablas necesarias existan"""
    tablas_requeridas = ['alimento', 'muestreo', 'parametros', 'siembra', 'usuarios']
    
    try:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SHOW TABLES")
        tablas_existentes = [tabla[0] for tabla in cursor.fetchall()]
        
        print("📊 Verificación de tablas:")
        for tabla in tablas_requeridas:
            if tabla in tablas_existentes:
                print(f"✅ Tabla '{tabla}' encontrada")
            else:
                print(f"❌ Tabla '{tabla}' NO encontrada")
        
        cursor.close()
        conn.close()
        
        return all(tabla in tablas_existentes for tabla in tablas_requeridas)
        
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

if __name__ == "__main__":
    print("🗄️ PRUEBA DE CONEXIÓN A BASE DE DATOS")
    print("=====================================")
    
    # Probar conexión
    success, message = DatabaseConfig.test_connection()
    print(f"Estado: {'✅ Exitoso' if success else '❌ Error'}")
    print(f"Mensaje: {message}")
    
    if success:
        # Obtener información del servidor
        info = DatabaseConfig.get_server_info()
        print(f"\n📋 Información del servidor:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        # Verificar tablas
        print(f"\n📊 Verificando tablas...")
        verificar_tablas()
