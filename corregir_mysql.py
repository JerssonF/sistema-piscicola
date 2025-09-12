#!/usr/bin/env python3
"""
Script para verificar y corregir la estructura de tablas MySQL
"""
import mysql.connector
from mysql.connector import Error
from database_config_mysql import get_mysql_connection

def verificar_estructura_mysql():
    """Verifica la estructura actual de las tablas"""
    
    print("🔍 VERIFICANDO ESTRUCTURA DE TABLAS MYSQL")
    print("=" * 50)
    
    conn = get_mysql_connection()
    if not conn:
        print("❌ No se pudo conectar a MySQL")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verificar tablas existentes
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()
        
        print(f"📋 Tablas encontradas: {len(tablas)}")
        for tabla in tablas:
            print(f"   - {tabla[0]}")
        
        # Verificar estructura de cada tabla
        for tabla_tuple in tablas:
            tabla = tabla_tuple[0]
            print(f"\n🔧 Estructura de tabla '{tabla}':")
            cursor.execute(f"DESCRIBE {tabla}")
            columnas = cursor.fetchall()
            
            for columna in columnas:
                print(f"   {columna[0]} | {columna[1]} | {columna[2]} | {columna[3]} | {columna[4]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"❌ Error: {e}")
        if conn.is_connected():
            conn.close()
        return False

def corregir_estructura_mysql():
    """Corrige la estructura de las tablas para que coincidan con SQLite"""
    
    print("\n🔧 CORRIGIENDO ESTRUCTURA DE TABLAS")
    print("=" * 50)
    
    conn = get_mysql_connection()
    if not conn:
        print("❌ No se pudo conectar a MySQL")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Eliminar y recrear tabla alimento con estructura correcta
        print("🍽️  Corrigiendo tabla alimento...")
        cursor.execute("DROP TABLE IF EXISTS alimento")
        cursor.execute('''
            CREATE TABLE alimento (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque VARCHAR(50) NOT NULL,
                tipo_alimento VARCHAR(100) NOT NULL,
                cantidad_kg DECIMAL(10,2) NOT NULL,
                observaciones TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                frecuencia_toma VARCHAR(100),
                mortalidad INT DEFAULT 0,
                causa_mortalidad TEXT,
                acciones_correctivas TEXT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Corrigir tabla muestreo
        print("🔬 Corrigiendo tabla muestreo...")
        cursor.execute("DROP TABLE IF EXISTS muestreo")
        cursor.execute('''
            CREATE TABLE muestreo (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque VARCHAR(50) NOT NULL,
                peso_promedio DECIMAL(10,2) NOT NULL,
                talla_promedio DECIMAL(10,2) NOT NULL,
                cantidad_peces INT NOT NULL,
                observaciones TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                frecuencia_toma VARCHAR(100),
                especie VARCHAR(100),
                biomasa DECIMAL(10,2),
                peces INT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Corrigir tabla parametros
        print("⚙️  Corrigiendo tabla parametros...")
        cursor.execute("DROP TABLE IF EXISTS parametros")
        cursor.execute('''
            CREATE TABLE parametros (
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                frecuencia_toma VARCHAR(100),
                oxigeno_disuelto DECIMAL(5,2),
                nitritos DECIMAL(5,2)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Corrigir tabla siembra
        print("🌱 Corrigiendo tabla siembra...")
        cursor.execute("DROP TABLE IF EXISTS siembra")
        cursor.execute('''
            CREATE TABLE siembra (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque VARCHAR(50) NOT NULL,
                especie VARCHAR(100) NOT NULL,
                cantidad INT NOT NULL,
                peso_promedio DECIMAL(10,2) NOT NULL,
                proveedor VARCHAR(100),
                observaciones TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                destino VARCHAR(100),
                ovas_alevinos INT,
                hembras_machos VARCHAR(50)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Estructura de tablas corregida")
        return True
        
    except Error as e:
        print(f"❌ Error corrigiendo estructura: {e}")
        if conn.is_connected():
            conn.close()
        return False

def insertar_datos_prueba():
    """Inserta algunos datos de prueba"""
    
    print("\n📝 INSERTANDO DATOS DE PRUEBA")
    print("=" * 50)
    
    conn = get_mysql_connection()
    if not conn:
        print("❌ No se pudo conectar a MySQL")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Insertar datos de prueba en alimento
        datos_alimento = [
            ('2025-09-05', '08:00', '1', 'Pellet Premium', 15.50, 'Datos de prueba MySQL', 'Cada 2 horas', 0, '', ''),
            ('2025-09-05', '14:00', '2', 'Concentrado', 20.00, 'Alimentación vespertina', 'Cada 3 horas', 1, 'Temperatura', 'Monitorear agua')
        ]
        
        for dato in datos_alimento:
            cursor.execute('''
                INSERT INTO alimento (fecha, hora, estanque, tipo_alimento, cantidad_kg, observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', dato)
        
        # Insertar datos de prueba en muestreo
        datos_muestreo = [
            ('2025-09-05', '10:00', '1', 150.5, 12.3, 100, 'Muestreo de prueba MySQL'),
        ]
        
        for dato in datos_muestreo:
            cursor.execute('''
                INSERT INTO muestreo (fecha, hora, estanque, peso_promedio, talla_promedio, cantidad_peces, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', dato)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Datos de prueba insertados")
        return True
        
    except Error as e:
        print(f"❌ Error insertando datos: {e}")
        if conn.is_connected():
            conn.close()
        return False

def main():
    """Función principal"""
    print("🔧 CONFIGURACIÓN FINAL DE MYSQL")
    print("=" * 50)
    
    # Verificar estructura actual
    verificar_estructura_mysql()
    
    # Corregir estructura
    if corregir_estructura_mysql():
        # Insertar datos de prueba
        if insertar_datos_prueba():
            print("\n🎉 ¡CONFIGURACIÓN MYSQL COMPLETADA!")
            print("\n📍 PRÓXIMOS PASOS:")
            print("   1. Ejecuta: python app_mysql.py")
            print("   2. Ve a phpMyAdmin → base de datos 'piscicola'")
            print("   3. Verás todas las tablas con los datos")
            print("   4. Los formularios web ahora guardarán en MySQL")
        else:
            print("❌ Error insertando datos de prueba")
    else:
        print("❌ Error corrigiendo estructura")

if __name__ == "__main__":
    main()
