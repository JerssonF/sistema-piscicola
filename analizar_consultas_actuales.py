#!/usr/bin/env python3
import sqlite3

def comparar_consultas_actuales():
    """Comparar las consultas actuales vs. lo que realmente devuelven"""
    
    print("🔍 ANALIZANDO CONSULTAS SQL ACTUALES")
    print("=" * 80)
    
    conn = sqlite3.connect('piscicola.db')
    cursor = conn.cursor()
    
    # La consulta actual del app.py para alimentos
    consulta_actual = """
        SELECT ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as '#', 
               fecha, frecuencia_toma, estanque as estanque_celda, 
               tipo_alimento as referencia_alimento, cantidad_kg as cantidad_alimento, 
               mortalidad, causa_mortalidad, acciones_correctivas 
        FROM alimento 
        WHERE 1=1 
        ORDER BY fecha DESC 
        LIMIT 2
    """
    
    print("📋 CONSULTA ACTUAL (ALIMENTOS):")
    print(consulta_actual)
    
    cursor.execute(consulta_actual)
    resultados = cursor.fetchall()
    columnas = [description[0] for description in cursor.description]
    
    print(f"\n📊 RESULTADOS ({len(resultados)} registros):")
    print("Columnas:", columnas)
    
    for i, registro in enumerate(resultados, 1):
        print(f"\n📝 Registro {i}:")
        for j, (col, val) in enumerate(zip(columnas, registro)):
            print(f"   {j+1}. {col}: {val}")
    
    # Verificar también los nombres que se mostrarán
    nombres_mostrados = ['#', 'Fecha', 'Frecuencia Toma', 'Estanque/Celda', 'Referencia Alimento', 'Cantidad Alimento', 'Mortalidad', 'Causa Mortalidad', 'Acciones Correctivas']
    
    print(f"\n🏷️  NOMBRES QUE SE MOSTRARÁN EN LA TABLA:")
    for i, nombre in enumerate(nombres_mostrados):
        col_bd = columnas[i] if i < len(columnas) else 'N/A'
        val_ejemplo = resultados[0][i] if resultados and i < len(resultados[0]) else 'N/A'
        print(f"   {i+1}. {nombre} -> {col_bd} = {val_ejemplo}")
    
    # Probar consulta para muestreo
    print(f"\n{'='*80}")
    print("📋 CONSULTA ACTUAL (MUESTREO):")
    
    consulta_muestreo = """
        SELECT ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as '#', 
               fecha, frecuencia_toma, especie, biomasa, 
               estanque as estanque_celda, peces, peso_promedio as peso_promedio_g 
        FROM muestreo 
        WHERE 1=1 
        ORDER BY fecha DESC 
        LIMIT 2
    """
    
    print(consulta_muestreo)
    
    cursor.execute(consulta_muestreo)
    resultados_muestreo = cursor.fetchall()
    columnas_muestreo = [description[0] for description in cursor.description]
    
    print(f"\n📊 RESULTADOS MUESTREO ({len(resultados_muestreo)} registros):")
    print("Columnas:", columnas_muestreo)
    
    if resultados_muestreo:
        print(f"\n📝 Primer registro:")
        for j, (col, val) in enumerate(zip(columnas_muestreo, resultados_muestreo[0])):
            print(f"   {j+1}. {col}: {val}")
    
    conn.close()

if __name__ == "__main__":
    comparar_consultas_actuales()
