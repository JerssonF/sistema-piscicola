#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from routes import get_db_connection

def test_datos():
    print("🔍 VERIFICANDO DATOS EN LA BASE DE DATOS...")
    
    conn = get_db_connection()
    if not conn:
        print("❌ No se pudo conectar a la base de datos")
        return
    
    cursor = conn.cursor(dictionary=True)
    
    tablas = ['alimento', 'ingreso_alimentos', 'muestreo', 'parametros', 'siembra']
    
    for tabla in tablas:
        try:
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) as total FROM {tabla}")
            total = cursor.fetchone()['total']
            
            print(f"\n=== {tabla.upper()} ===")
            print(f"Total registros: {total}")
            
            if total > 0:
                # Mostrar algunos registros
                cursor.execute(f"SELECT * FROM {tabla} ORDER BY fecha DESC LIMIT 2")
                registros = cursor.fetchall()
                
                for i, reg in enumerate(registros, 1):
                    print(f"  Registro {i}: {dict(reg)}")
            
        except Exception as e:
            print(f"❌ Error en tabla {tabla}: {e}")
    
    conn.close()

def test_filtro_especifico():
    print("\n🔍 PROBANDO FILTRO POR TABLA ESPECÍFICA...")
    
    conn = get_db_connection()
    if not conn:
        print("❌ No se pudo conectar a la base de datos")
        return
    
    cursor = conn.cursor(dictionary=True)
    
    # Probar filtro por alimento
    try:
        query = "SELECT *, 'alimento' as tipo FROM alimento WHERE 1=1 ORDER BY fecha DESC LIMIT 200"
        print(f"📋 Ejecutando: {query}")
        cursor.execute(query)
        resultados = cursor.fetchall()
        print(f"✅ Registros encontrados en alimento: {len(resultados)}")
        
        for reg in resultados:
            print(f"  {dict(reg)}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    conn.close()

if __name__ == "__main__":
    test_datos()
    test_filtro_especifico()
