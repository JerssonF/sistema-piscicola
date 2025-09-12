#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import requests

def verificar_datos_reales():
    """Verifica los datos reales vs lo que muestra el formulario"""
    
    print("🔍 VERIFICACIÓN DE DATOS REALES DE PHPMY ADMIN")
    print("=" * 70)
    
    # 1. Verificar datos en la base de datos local
    print("1️⃣ DATOS EN BASE DE DATOS LOCAL:")
    conn = sqlite3.connect('piscicola.db')
    cursor = conn.cursor()
    
    # Obtener todos los datos ordenados por fecha
    cursor.execute("""
        SELECT fecha, frecuencia_toma, estanque, tipo_alimento, 
               cantidad_kg, mortalidad, causa_mortalidad, acciones_correctivas,
               created_at
        FROM alimento 
        ORDER BY fecha DESC
    """)
    
    registros_bd = cursor.fetchall()
    columns = ['fecha', 'frecuencia_toma', 'estanque', 'tipo_alimento', 
               'cantidad_kg', 'mortalidad', 'causa_mortalidad', 'acciones_correctivas', 'created_at']
    
    print(f"   📊 Total registros en BD: {len(registros_bd)}")
    
    for i, row in enumerate(registros_bd, 1):
        print(f"\n   📄 REGISTRO {i}:")
        for col, val in zip(columns, row):
            if col in ['mortalidad', 'causa_mortalidad', 'acciones_correctivas']:
                print(f"      🎯 {col}: {val}")
            else:
                print(f"         {col}: {val}")
    
    conn.close()
    
    # 2. Verificar lo que devuelve el endpoint
    print(f"\n2️⃣ DATOS DEL ENDPOINT CON RANGO AMPLIO:")
    
    try:
        url = "http://127.0.0.1:5000/filtrar_informes"
        params = {
            'formulario': 'alimento',
            'fecha_inicio': '2025-01-01',  # Rango muy amplio
            'fecha_fin': '2025-12-31'
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            datos_endpoint = data.get('datos', [])
            
            print(f"   📊 Total registros endpoint: {len(datos_endpoint)}")
            print(f"   📋 Columnas SQL: {data.get('columnas_sql', [])}")
            
            for i, registro in enumerate(datos_endpoint, 1):
                print(f"\n   📄 REGISTRO ENDPOINT {i}:")
                for key, val in registro.items():
                    if key in ['mortalidad', 'causa_mortalidad', 'acciones_correctivas']:
                        print(f"      🎯 {key}: {val}")
                    else:
                        print(f"         {key}: {val}")
        else:
            print(f"   ❌ Error en endpoint: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error conectando al endpoint: {e}")
    
    # 3. Comparación específica de registros con mortalidad
    print(f"\n3️⃣ COMPARACIÓN DE REGISTROS CON MORTALIDAD:")
    
    # Datos que aparecen en phpMyAdmin (según la imagen)
    datos_phpmyadmin = [
        {'fecha': '2025-08-26', 'mortalidad': 2, 'causa': 'Enfermedad', 'acciones': 'Aumentar oxigenación'},
        {'fecha': '2025-08-25', 'mortalidad': 0, 'causa': '', 'acciones': 'Mantener rutina'},
        {'fecha': '2025-08-24', 'mortalidad': 1, 'causa': 'Estrés', 'acciones': 'Revisar temperatura'},
        {'fecha': '2025-08-21', 'mortalidad': 56456, 'causa': 'sadsd', 'acciones': 'dvcxv'},
        {'fecha': '2025-08-07', 'mortalidad': 4, 'causa': 'sdfdsd', 'acciones': 'aza'},
        {'fecha': '2025-08-14', 'mortalidad': 4, 'causa': 'asadsdsf', 'acciones': 'dfsdsfdsfds'},
        {'fecha': '2025-08-30', 'mortalidad': 1200, 'causa': 'Estres', 'acciones': 'Ampliar lago'}
    ]
    
    print(f"   📊 DATOS ESPERADOS (phpMyAdmin):")
    for dato in datos_phpmyadmin:
        print(f"      {dato['fecha']}: mort={dato['mortalidad']}, causa='{dato['causa']}', acciones='{dato['acciones']}'")
    
    # 4. Verificar si estos datos específicos están en la BD local
    print(f"\n4️⃣ VERIFICANDO DATOS ESPECÍFICOS EN BD LOCAL:")
    
    conn = sqlite3.connect('piscicola.db')
    cursor = conn.cursor()
    
    for dato in datos_phpmyadmin:
        cursor.execute("""
            SELECT fecha, mortalidad, causa_mortalidad, acciones_correctivas 
            FROM alimento 
            WHERE fecha = ? AND mortalidad = ?
        """, (dato['fecha'], dato['mortalidad']))
        
        resultado = cursor.fetchone()
        if resultado:
            print(f"      ✅ {dato['fecha']}: ENCONTRADO - mort={resultado[1]}, causa='{resultado[2]}', acciones='{resultado[3]}'")
        else:
            print(f"      ❌ {dato['fecha']}: NO ENCONTRADO con mortalidad={dato['mortalidad']}")
    
    conn.close()
    
    # 5. Verificar si hay diferencias en las bases de datos
    print(f"\n5️⃣ POSIBLES PROBLEMAS:")
    print(f"   🔍 Verificar si:")
    print(f"      1. La BD local está actualizada con los datos de phpMyAdmin")
    print(f"      2. Las fechas de filtro incluyen todos los registros")
    print(f"      3. Hay problemas de sincronización entre BD local y remota")
    print(f"      4. Los datos se insertaron después de la última sincronización")

if __name__ == "__main__":
    verificar_datos_reales()
