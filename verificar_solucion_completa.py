#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re

def verificar_solucion():
    """Verifica si la solución está implementada correctamente"""
    
    print("🔧 VERIFICACIÓN DE LA SOLUCIÓN IMPLEMENTADA")
    print("=" * 60)
    
    # 1. Verificar que el backend envía columnas_sql correctamente
    print("1️⃣ VERIFICANDO BACKEND...")
    url = "http://127.0.0.1:5000/filtrar_informes"
    params = {
        'formulario': 'alimento',
        'fecha_inicio': '2025-08-01',
        'fecha_fin': '2025-08-31'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data.get('columnas_sql'):
        print(f"   ✅ Backend envía columnas_sql: {data['columnas_sql']}")
        columnas_backend = data['columnas_sql']
    else:
        print(f"   ❌ Backend NO envía columnas_sql")
        return False
    
    # 2. Verificar que el frontend está configurado para usar columnas_sql
    print("\n2️⃣ VERIFICANDO FRONTEND...")
    
    with open('templates/formulario_informes_nuevo.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Buscar la línea específica que usa columnas_sql
    patron_columnas_sql = r'window\.currentResponse\.columnas_sql'
    if re.search(patron_columnas_sql, html_content):
        print(f"   ✅ Frontend configurado para usar window.currentResponse.columnas_sql")
        
        # Extraer la línea específica
        lineas = html_content.split('\n')
        for i, linea in enumerate(lineas):
            if 'window.currentResponse.columnas_sql' in linea:
                print(f"   📝 Línea {i+1}: {linea.strip()}")
    else:
        print(f"   ❌ Frontend NO configurado para usar columnas_sql")
        return False
    
    # 3. Verificar que no se está usando Object.keys() como fallback principal
    patron_object_keys = r'Object\.keys\(datos\[0\]\)'
    matches_object_keys = re.findall(patron_object_keys, html_content)
    
    if matches_object_keys:
        print(f"\n   ⚠️  Se encontraron {len(matches_object_keys)} usos de Object.keys(datos[0])")
        
        # Buscar el contexto de cada uso
        lineas = html_content.split('\n')
        for i, linea in enumerate(lineas):
            if 'Object.keys(datos[0])' in linea:
                print(f"   📝 Línea {i+1}: {linea.strip()}")
    
    # 4. Verificar los datos reales
    print("\n3️⃣ VERIFICANDO DATOS REALES...")
    
    datos = data.get('datos', [])
    if datos:
        primer_registro = datos[0]
        
        # Verificar orden de claves en JSON vs columnas_sql
        claves_json = list(primer_registro.keys())
        claves_backend = columnas_backend
        
        print(f"   🔑 Claves en JSON: {claves_json}")
        print(f"   📋 Orden backend:  {claves_backend}")
        
        if claves_json == claves_backend:
            print(f"   ✅ ORDEN CONSISTENTE")
        else:
            print(f"   ⚠️  ORDEN DIFERENTE - Aquí está el problema")
            
            # Mostrar diferencias específicas
            print(f"\n   🔍 ANÁLISIS DE DIFERENCIAS:")
            
            # Posiciones de las columnas problemáticas
            columnas_problema = ['mortalidad', 'causa_mortalidad', 'acciones_correctivas']
            
            for col in columnas_problema:
                pos_json = claves_json.index(col) + 1 if col in claves_json else 'NO ENCONTRADA'
                pos_backend = claves_backend.index(col) + 1 if col in claves_backend else 'NO ENCONTRADA'
                valor = primer_registro.get(col, 'N/A')
                
                print(f"   📊 {col}:")
                print(f"      JSON posición: {pos_json}")
                print(f"      Backend posición: {pos_backend}")
                print(f"      Valor: {valor}")
    
    # 5. Recomendaciones
    print(f"\n4️⃣ RECOMENDACIONES:")
    
    if claves_json != claves_backend:
        print(f"   🔧 SOLUCIÓN:")
        print(f"   1. El frontend DEBE usar window.currentResponse.columnas_sql")
        print(f"   2. NO debe usar Object.keys(datos[0]) como fallback")
        print(f"   3. Verificar que window.currentResponse se asigna correctamente")
        
        # Verificar la asignación de window.currentResponse
        patron_assignment = r'window\.currentResponse\s*=\s*data'
        if re.search(patron_assignment, html_content):
            print(f"   ✅ Asignación window.currentResponse = data encontrada")
        else:
            print(f"   ❌ Asignación window.currentResponse = data NO encontrada")
    else:
        print(f"   ✅ No se requieren cambios adicionales")

if __name__ == "__main__":
    verificar_solucion()
