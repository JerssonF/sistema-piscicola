#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICAR ESTRUCTURA DE TABLAS MYSQL
====================================
Script para verificar la estructura real de las tablas en MySQL.
"""

import mysql.connector
from mysql.connector import Error

def verificar_estructura_tablas():
    """Verificar la estructura de todas las tablas"""
    
    try:
        # Conectar a MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='piscicola'
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Obtener lista de tablas
            cursor.execute("SHOW TABLES")
            tablas = cursor.fetchall()
            
            print("🔍 ESTRUCTURA DE TABLAS EN MySQL")
            print("=" * 60)
            
            for (tabla_nombre,) in tablas:
                print(f"\n📋 TABLA: {tabla_nombre}")
                print("-" * 40)
                
                # Obtener estructura de la tabla
                cursor.execute(f"DESCRIBE {tabla_nombre}")
                columnas = cursor.fetchall()
                
                for columna in columnas:
                    field, tipo, null, key, default, extra = columna
                    print(f"  • {field} ({tipo})")
                
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {tabla_nombre}")
                count = cursor.fetchone()[0]
                print(f"  📊 Registros: {count}")
                
                # Mostrar algunos datos de ejemplo
                if count > 0:
                    cursor.execute(f"SELECT * FROM {tabla_nombre} LIMIT 3")
                    ejemplos = cursor.fetchall()
                    print(f"  📝 Ejemplos:")
                    for i, ejemplo in enumerate(ejemplos, 1):
                        print(f"    {i}. {ejemplo}")
            
            cursor.close()
            conn.close()
            print(f"\n✅ Verificación completada")
            
    except Error as e:
        print(f"❌ Error de MySQL: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_estructura_tablas()
