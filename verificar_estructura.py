#!/usr/bin/env python3
import sqlite3

def verificar_estructura_tablas():
    """Verificar la estructura de todas las tablas"""
    try:
        conn = sqlite3.connect('piscicola.db')
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = [row[0] for row in cursor.fetchall()]
        
        print("📋 ESTRUCTURA DE LAS TABLAS EN LA BASE DE DATOS")
        print("="*60)
        
        for tabla in tablas:
            if tabla != 'sqlite_sequence':  # Ignorar tabla sistema
                print(f"\n🗂️  TABLA: {tabla.upper()}")
                print("-" * 40)
                
                cursor.execute(f"PRAGMA table_info({tabla})")
                columnas = cursor.fetchall()
                
                for col in columnas:
                    col_id, nombre, tipo, not_null, default, pk = col
                    pk_text = " (PK)" if pk else ""
                    not_null_text = " NOT NULL" if not_null else ""
                    default_text = f" DEFAULT {default}" if default else ""
                    
                    print(f"  {col_id+1:2}. {nombre:<20} {tipo:<10}{pk_text}{not_null_text}{default_text}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_estructura_tablas()
