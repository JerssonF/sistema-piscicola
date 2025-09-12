#!/usr/bin/env python3
"""
Verificar estructura de la tabla alimento para corregir el error
"""
import mysql.connector
from database_config_mysql import get_mysql_connection

def verificar_estructura_tabla():
    """Verifica la estructura actual de la tabla alimento"""
    
    print("🔍 VERIFICANDO ESTRUCTURA DE TABLA ALIMENTO")
    print("=" * 60)
    
    conn = get_mysql_connection()
    if not conn:
        print("❌ No se puede conectar a MySQL")
        return
    
    try:
        cursor = conn.cursor()
        
        # Describir la tabla alimento
        cursor.execute("DESCRIBE alimento")
        columnas = cursor.fetchall()
        
        print("📋 Estructura actual de la tabla 'alimento':")
        print("   Campo                | Tipo         | Null | Key | Default | Extra")
        print("   " + "-" * 65)
        
        for col in columnas:
            campo, tipo, null_val, key, default, extra = col
            print(f"   {campo:<20} | {tipo:<12} | {null_val:<4} | {key:<3} | {str(default):<7} | {extra}")
        
        print(f"\n   📊 Total de columnas: {len(columnas)}")
        
        # Mostrar la consulta problemática
        print("\n🚨 PROBLEMA DETECTADO:")
        print("   La consulta SQL en app_mysql.py intenta insertar en 10 columnas:")
        consulta_problema = '''INSERT INTO alimento (fecha, hora, estanque, tipo_alimento, cantidad_kg, observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas)'''
        print(f"   {consulta_problema}")
        
        # Verificar qué columnas faltan
        columnas_esperadas = ['fecha', 'hora', 'estanque', 'tipo_alimento', 'cantidad_kg', 'observaciones', 'frecuencia_toma', 'mortalidad', 'causa_mortalidad', 'acciones_correctivas']
        columnas_existentes = [col[0] for col in columnas]
        
        print(f"\n   📝 Columnas que faltan:")
        for col in columnas_esperadas:
            if col not in columnas_existentes:
                print(f"      ❌ {col}")
        
        print(f"\n   ✅ Columnas que existen:")
        for col in columnas_esperadas:
            if col in columnas_existentes:
                print(f"      ✅ {col}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if conn.is_connected():
            conn.close()

def agregar_columnas_faltantes():
    """Agrega las columnas que faltan a la tabla alimento"""
    
    print("\n🔧 AGREGANDO COLUMNAS FALTANTES")
    print("=" * 60)
    
    conn = get_mysql_connection()
    if not conn:
        print("❌ No se puede conectar a MySQL")
        return
    
    try:
        cursor = conn.cursor()
        
        # Columnas a agregar
        columnas_agregar = [
            "ALTER TABLE alimento ADD COLUMN frecuencia_toma VARCHAR(100) DEFAULT ''",
            "ALTER TABLE alimento ADD COLUMN mortalidad INT DEFAULT 0",
            "ALTER TABLE alimento ADD COLUMN causa_mortalidad TEXT DEFAULT ''",
            "ALTER TABLE alimento ADD COLUMN acciones_correctivas TEXT DEFAULT ''"
        ]
        
        for sql in columnas_agregar:
            try:
                cursor.execute(sql)
                print(f"   ✅ {sql}")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    print(f"   ⚠️  Columna ya existe: {sql}")
                else:
                    print(f"   ❌ Error: {sql} - {e}")
        
        conn.commit()
        print("\n✅ Columnas agregadas correctamente")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if conn.is_connected():
            conn.close()

def main():
    verificar_estructura_tabla()
    agregar_columnas_faltantes()
    
    print(f"\n{'='*60}")
    print("✅ CORRECCIÓN COMPLETADA")
    print("   Ahora el formulario debería guardar correctamente")
    print("=" * 60)

if __name__ == "__main__":
    main()
