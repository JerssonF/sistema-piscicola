#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import requests
import json
from collections import OrderedDict

def analizar_discrepancia_datos():
    """Analiza las discrepancias entre los datos de BD y la tabla de resultados"""
    
    print("🔍 ANÁLISIS EXHAUSTIVO DE DISCREPANCIAS")
    print("=" * 70)
    
    # 1. Obtener datos DIRECTAMENTE de la base de datos
    print("1️⃣ OBTENIENDO DATOS DIRECTOS DE LA BASE DE DATOS...")
    conn = sqlite3.connect('piscicola.db')
    cursor = conn.cursor()
    
    # Ejecutar la consulta exacta que usa el backend
    query_alimento = """
    SELECT 
        ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as '#',
        fecha,
        frecuencia_toma,
        estanque as estanque_celda,
        tipo_alimento as referencia_alimento,
        cantidad_kg as cantidad_alimento,
        mortalidad,
        causa_mortalidad,
        acciones_correctivas
    FROM alimento 
    WHERE fecha BETWEEN '2025-08-01' AND '2025-08-31'
    ORDER BY fecha DESC, hora DESC
    """
    
    cursor.execute(query_alimento)
    rows_bd = cursor.fetchall()
    columns_bd = [description[0] for description in cursor.description]
    
    print(f"   📊 Registros en BD: {len(rows_bd)}")
    print(f"   📋 Columnas en BD: {columns_bd}")
    
    if rows_bd:
        print(f"\n   📄 PRIMER REGISTRO EN BD:")
        for i, (col, val) in enumerate(zip(columns_bd, rows_bd[0]), 1):
            print(f"      {i}. {col}: {val}")
        
        print(f"\n   📄 TODOS LOS REGISTROS EN BD:")
        for idx, row in enumerate(rows_bd, 1):
            print(f"   Registro {idx}:")
            for col, val in zip(columns_bd, row):
                print(f"      {col}: {val}")
            print()
    
    conn.close()
    
    # 2. Obtener datos del ENDPOINT
    print("2️⃣ OBTENIENDO DATOS DEL ENDPOINT...")
    url = "http://127.0.0.1:5000/filtrar_informes"
    params = {
        'formulario': 'alimento',
        'fecha_inicio': '2025-08-01',
        'fecha_fin': '2025-08-31'
    }
    
    try:
        response = requests.get(url, params=params)
        data_endpoint = response.json()
        
        print(f"   📊 Registros en endpoint: {data_endpoint.get('total', 0)}")
        print(f"   📋 Columnas SQL: {data_endpoint.get('columnas_sql', [])}")
        
        datos_endpoint = data_endpoint.get('datos', [])
        
        if datos_endpoint:
            print(f"\n   📄 PRIMER REGISTRO EN ENDPOINT:")
            primer_registro = datos_endpoint[0]
            for i, (key, val) in enumerate(primer_registro.items(), 1):
                print(f"      {i}. {key}: {val}")
            
            print(f"\n   📄 TODOS LOS REGISTROS EN ENDPOINT:")
            for idx, registro in enumerate(datos_endpoint, 1):
                print(f"   Registro {idx}:")
                for key, val in registro.items():
                    print(f"      {key}: {val}")
                print()
        
    except Exception as e:
        print(f"   ❌ Error obteniendo datos del endpoint: {e}")
        return
    
    # 3. COMPARACIÓN DETALLADA
    print("3️⃣ COMPARACIÓN DETALLADA BD vs ENDPOINT...")
    
    if len(rows_bd) != len(datos_endpoint):
        print(f"   ⚠️  DIFERENCIA EN CANTIDAD DE REGISTROS:")
        print(f"      BD: {len(rows_bd)} registros")
        print(f"      Endpoint: {len(datos_endpoint)} registros")
    else:
        print(f"   ✅ Misma cantidad de registros: {len(rows_bd)}")
    
    # Comparar registro por registro
    print(f"\n   🔍 COMPARACIÓN REGISTRO POR REGISTRO:")
    
    for i in range(min(len(rows_bd), len(datos_endpoint))):
        print(f"\n   📄 REGISTRO {i+1}:")
        row_bd = rows_bd[i]
        row_endpoint = datos_endpoint[i]
        
        # Crear diccionario de BD para comparar
        bd_dict = dict(zip(columns_bd, row_bd))
        
        print(f"      BD     : {bd_dict}")
        print(f"      Endpoint: {row_endpoint}")
        
        # Verificar cada campo
        discrepancias = []
        for col_bd, val_bd in bd_dict.items():
            if col_bd in row_endpoint:
                val_endpoint = row_endpoint[col_bd]
                if str(val_bd) != str(val_endpoint):
                    discrepancias.append(f"{col_bd}: BD='{val_bd}' vs Endpoint='{val_endpoint}'")
            else:
                discrepancias.append(f"{col_bd}: Falta en endpoint")
        
        # Verificar campos adicionales en endpoint
        for col_endpoint in row_endpoint:
            if col_endpoint not in bd_dict:
                discrepancias.append(f"{col_endpoint}: Extra en endpoint")
        
        if discrepancias:
            print(f"      ⚠️  DISCREPANCIAS:")
            for disc in discrepancias:
                print(f"         {disc}")
        else:
            print(f"      ✅ REGISTRO IDÉNTICO")
    
    # 4. Verificar campos específicos que el usuario menciona
    print(f"\n4️⃣ VERIFICACIÓN DE CAMPOS ESPECÍFICOS...")
    
    campos_criticos = ['mortalidad', 'causa_mortalidad', 'acciones_correctivas']
    
    if datos_endpoint:
        for campo in campos_criticos:
            print(f"\n   🔍 CAMPO '{campo}':")
            
            # Verificar en BD
            if campo in columns_bd:
                idx_bd = columns_bd.index(campo)
                valores_bd = [row[idx_bd] for row in rows_bd]
                print(f"      BD valores: {valores_bd}")
            else:
                print(f"      BD: Campo no encontrado")
            
            # Verificar en endpoint
            valores_endpoint = []
            for registro in datos_endpoint:
                if campo in registro:
                    valores_endpoint.append(registro[campo])
                else:
                    valores_endpoint.append('NO_ENCONTRADO')
            
            print(f"      Endpoint valores: {valores_endpoint}")
            
            # Verificar si coinciden
            if campo in columns_bd:
                valores_bd_str = [str(v) for v in valores_bd]
                valores_endpoint_str = [str(v) for v in valores_endpoint]
                
                if valores_bd_str == valores_endpoint_str:
                    print(f"      ✅ VALORES COINCIDEN")
                else:
                    print(f"      ❌ VALORES NO COINCIDEN")
    
    # 5. Verificar estructura de respuesta completa
    print(f"\n5️⃣ ESTRUCTURA COMPLETA DE RESPUESTA DEL ENDPOINT:")
    print(f"   🔧 Claves principales: {list(data_endpoint.keys())}")
    
    for key, value in data_endpoint.items():
        if key != 'datos':  # Los datos ya los vimos arriba
            print(f"   📋 {key}: {value}")

if __name__ == "__main__":
    analizar_discrepancia_datos()
