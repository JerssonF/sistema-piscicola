#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear las tablas de la base de datos piscicola
Ejecutar este script antes de usar la aplicación
"""

import mysql.connector
from mysql.connector import Error
from config import Config

def create_database_tables():
    """Crear todas las tablas necesarias para la aplicación piscicola"""
    
    # Configuración de conexión
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Cambiar si tienes contraseña
        'database': 'piscicola'
    }
    
    # SQL para crear las tablas
    create_tables_sql = [
        """
        CREATE TABLE IF NOT EXISTS alimento (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha DATE NOT NULL,
            frecuencia_toma VARCHAR(100),
            estanque_celda VARCHAR(50),
            referencia_alimento VARCHAR(100),
            cantidad_alimento DECIMAL(10,2),
            mortalidad INT,
            causa_mortalidad TEXT,
            acciones_correctivas TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        
        """
        CREATE TABLE IF NOT EXISTS ingreso_alimentos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha DATE NOT NULL,
            hora TIME NOT NULL,
            ingreso_comida VARCHAR(100),
            cantidad DECIMAL(10,2),
            transporte VARCHAR(100),
            observaciones TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        
        """
        CREATE TABLE IF NOT EXISTS muestreo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha DATE NOT NULL,
            frecuencia_toma VARCHAR(100),
            especie VARCHAR(100),
            biomasa DECIMAL(10,2),
            estanque_celda VARCHAR(50),
            peces INT,
            peso_promedio_g DECIMAL(10,2),
            promedio_total_g DECIMAL(10,2),
            acciones_correctivas TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        
        """
        CREATE TABLE IF NOT EXISTS parametros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha DATE NOT NULL,
            hora TIME NOT NULL,
            estanque_celda VARCHAR(50),
            oxigeno DECIMAL(5,2),
            temperatura DECIMAL(5,2),
            ph DECIMAL(3,1),
            amonio DECIMAL(5,2),
            observaciones TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        
        """
        CREATE TABLE IF NOT EXISTS siembra (
            id INT AUTO_INCREMENT PRIMARY KEY,
            frecuencia_toma VARCHAR(100),
            fecha DATE NOT NULL,
            hora_siembra TIME NOT NULL,
            origen_semilla VARCHAR(100),
            codigo_trazabilidad VARCHAR(100),
            especie VARCHAR(100),
            destino VARCHAR(100),
            hembras_machos VARCHAR(50),
            ovas_alevinos INT,
            peso_promedio DECIMAL(5,2),
            biomasa DECIMAL(10,2),
            estanque_celda VARCHAR(50),
            acciones_correctivas TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    ]
    
    try:
        # Conectar a MySQL
        print("🔄 Conectando a MySQL...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor()
            print("✅ Conexión exitosa a MySQL")
            
            # Crear cada tabla
            for i, sql in enumerate(create_tables_sql, 1):
                try:
                    cursor.execute(sql)
                    table_name = ['alimento', 'ingreso_alimentos', 'muestreo', 'parametros', 'siembra'][i-1]
                    print(f"✅ Tabla '{table_name}' creada correctamente")
                except Error as e:
                    print(f"❌ Error creando tabla {i}: {e}")
            
            # Confirmar cambios
            connection.commit()
            print("\n🎉 ¡Todas las tablas han sido creadas exitosamente!")
            
            # Mostrar tablas existentes
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("\n📋 Tablas en la base de datos 'piscicola':")
            for table in tables:
                print(f"   - {table[0]}")
                
    except Error as e:
        print(f"❌ Error de conexión a MySQL: {e}")
        print("\n💡 Soluciones posibles:")
        print("   1. Verificar que MySQL esté ejecutándose")
        print("   2. Verificar usuario y contraseña")
        print("   3. Crear la base de datos 'piscicola' primero")
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\n🔒 Conexión cerrada")

def create_database():
    """Crear la base de datos piscicola si no existe"""
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': ''  # Cambiar si tienes contraseña
    }
    
    try:
        print("🔄 Creando base de datos 'piscicola'...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS piscicola CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ Base de datos 'piscicola' creada/verificada")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error creando base de datos: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Configurando base de datos para aplicación piscicola\n")
    
    # Primero crear la base de datos
    if create_database():
        # Luego crear las tablas
        create_database_tables()
    
    print("\n✨ Script completado. La aplicación está lista para usar.")
