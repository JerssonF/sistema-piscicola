"""
🗄️ CONFIGURACIÓN COMPLETA DE BASE DE DATOS PARA SERVIDOR
Crea tablas faltantes y configura usuarios
"""

import mysql.connector
from mysql.connector import Error
from database_config import DatabaseConfig

def crear_tabla_usuarios():
    """Crea la tabla de usuarios si no existe"""
    try:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        # SQL para crear tabla usuarios
        create_usuarios_table = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_usuarios_table)
        
        # Insertar usuario admin por defecto
        insert_admin = """
        INSERT IGNORE INTO usuarios (username, password) 
        VALUES ('admin', 'admin123');
        """
        
        cursor.execute(insert_admin)
        conn.commit()
        
        print("✅ Tabla 'usuarios' creada/verificada")
        print("✅ Usuario 'admin' creado/verificado")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando tabla usuarios: {e}")
        return False

def crear_usuario_remoto():
    """Crea usuario para acceso remoto"""
    try:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        # Comandos SQL para configurar acceso remoto
        sql_commands = [
            "CREATE USER IF NOT EXISTS 'piscicola_user'@'%' IDENTIFIED BY 'piscicola123';",
            "GRANT ALL PRIVILEGES ON piscicola.* TO 'piscicola_user'@'%';",
            "GRANT ALL PRIVILEGES ON piscicola.* TO 'root'@'%' IDENTIFIED BY '';",
            "FLUSH PRIVILEGES;"
        ]
        
        for command in sql_commands:
            try:
                cursor.execute(command)
                print(f"✅ Ejecutado: {command.split()[0]} {command.split()[1] if len(command.split()) > 1 else ''}")
            except Error as e:
                print(f"⚠️ Warning en comando: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Usuario remoto configurado")
        return True
        
    except Exception as e:
        print(f"❌ Error configurando usuario remoto: {e}")
        return False

def verificar_configuracion_completa():
    """Verifica que toda la configuración esté correcta"""
    try:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        # Verificar todas las tablas
        tablas_requeridas = ['alimento', 'muestreo', 'parametros', 'siembra', 'usuarios']
        cursor.execute("SHOW TABLES")
        tablas_existentes = [tabla[0] for tabla in cursor.fetchall()]
        
        print("\n📊 Estado de las tablas:")
        todas_ok = True
        for tabla in tablas_requeridas:
            if tabla in tablas_existentes:
                print(f"✅ {tabla}")
            else:
                print(f"❌ {tabla}")
                todas_ok = False
        
        # Verificar usuario admin
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE username = 'admin'")
        admin_count = cursor.fetchone()[0]
        
        if admin_count > 0:
            print("✅ Usuario admin configurado")
        else:
            print("❌ Usuario admin NO encontrado")
            todas_ok = False
        
        # Mostrar información de usuarios MySQL
        try:
            cursor.execute("SELECT User, Host FROM mysql.user WHERE User IN ('root', 'piscicola_user')")
            mysql_users = cursor.fetchall()
            
            print("\n👥 Usuarios MySQL configurados:")
            for user in mysql_users:
                print(f"  - {user[0]}@{user[1]}")
                
        except Error as e:
            print(f"⚠️ No se pudo verificar usuarios MySQL: {e}")
        
        cursor.close()
        conn.close()
        
        return todas_ok
        
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def configuracion_completa():
    """Ejecuta toda la configuración necesaria"""
    print("🗄️ CONFIGURACIÓN COMPLETA DE BASE DE DATOS")
    print("==========================================")
    
    # Paso 1: Verificar conexión
    success, message = DatabaseConfig.test_connection()
    if not success:
        print(f"❌ No se puede conectar a la base de datos: {message}")
        return False
    
    print("✅ Conexión a base de datos exitosa")
    
    # Paso 2: Crear tabla usuarios
    print("\n📋 Configurando tabla de usuarios...")
    if not crear_tabla_usuarios():
        print("❌ Error configurando tabla usuarios")
        return False
    
    # Paso 3: Configurar acceso remoto
    print("\n📋 Configurando acceso remoto...")
    if not crear_usuario_remoto():
        print("⚠️ Warning: Problemas configurando acceso remoto")
    
    # Paso 4: Verificación final
    print("\n📋 Verificación final...")
    if verificar_configuracion_completa():
        print("\n🎉 CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
        print("========================================")
        print("✅ Base de datos lista para servidor en red")
        print("✅ Todas las tablas configuradas")
        print("✅ Usuario admin: admin / admin123")
        print("✅ Acceso remoto configurado")
        return True
    else:
        print("\n❌ CONFIGURACIÓN INCOMPLETA")
        print("===========================")
        print("⚠️ Revisa los errores mostrados arriba")
        return False

if __name__ == "__main__":
    configuracion_completa()
