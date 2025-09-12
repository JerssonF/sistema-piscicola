#!/usr/bin/env python3
"""
Script para verificar la estructura de todas las tablas en la base de datos
"""

import sqlite3
import os

def verificar_estructura_completa():
    """Verificar estructura de todas las tablas"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'piscicola.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("=" * 60)
        print("ESTRUCTURA COMPLETA DE LA BASE DE DATOS")
        print("=" * 60)
        
        for table in tables:
            table_name = table[0]
            
            if table_name == 'sqlite_sequence':
                continue
                
            print(f"\n📋 TABLA: {table_name.upper()}")
            print("-" * 40)
            
            # Obtener estructura de la tabla
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("Columnas:")
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                nullable = "NOT NULL" if not_null else "NULL"
                primary = "(PK)" if pk else ""
                print(f"  {col_id + 1:2d}. {col_name:<20} {col_type:<15} {nullable:<8} {primary}")
            
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\nRegistros: {count}")
            
            # Si es una tabla de datos (no usuarios), mostrar muestra
            if table_name != 'usuarios' and count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                sample_data = cursor.fetchall()
                print("\nMuestra de datos:")
                for i, row in enumerate(sample_data, 1):
                    print(f"  Registro {i}: {row}")
        
        conn.close()
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_estructura_completa()
