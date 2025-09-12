#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def simular_renderizado_frontend():
    """Simula exactamente cómo el frontend renderiza la tabla"""
    
    print("🖥️ SIMULACIÓN DEL RENDERIZADO FRONTEND")
    print("=" * 60)
    
    # 1. Obtener datos igual que el frontend
    print("1️⃣ OBTENIENDO DATOS (como hace el frontend)...")
    url = "http://127.0.0.1:5000/filtrar_informes"
    params = {
        'formulario': 'alimento',
        'fecha_inicio': '2025-08-01',
        'fecha_fin': '2025-09-30'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # 2. Simular window.currentResponse = data
    current_response = data
    
    # 3. Simular mostrarResultados() con la lógica CORREGIDA
    print("2️⃣ SIMULANDO mostrarResultados()...")
    
    datos = data.get('datos', [])
    columnas = data.get('columnas', [])
    total = data.get('total', 0)
    formulario = 'alimento'
    
    # LÓGICA CORREGIDA: columnasData primero
    columnas_data = current_response.get('columnas_sql') if current_response and current_response.get('columnas_sql') else list(datos[0].keys())
    
    # LÓGICA CORREGIDA: nombresColumnas usa columnasData
    nombres_columnas = columnas or [format_column_name(col) for col in columnas_data]
    
    print(f"   📋 columnas_data: {columnas_data}")
    print(f"   🏷️  nombres_columnas: {nombres_columnas}")
    print(f"   📊 total registros: {total}")
    
    # 4. Simular la construcción de la tabla HTML
    print(f"\n3️⃣ SIMULANDO CONSTRUCCIÓN DE TABLA HTML...")
    
    # Crear encabezado
    print(f"   📋 ENCABEZADOS DE TABLA:")
    for i, nombre in enumerate(nombres_columnas, 1):
        print(f"      {i}. <th>{nombre}</th>")
    
    # Crear filas de datos
    print(f"\n   📄 FILAS DE DATOS:")
    for idx, registro in enumerate(datos, 1):
        print(f"   \n   FILA {idx}:")
        for i, col_key in enumerate(columnas_data, 1):
            valor = registro.get(col_key, 'NO ENCONTRADO')
            nombre_col = nombres_columnas[i-1] if i-1 < len(nombres_columnas) else 'SIN NOMBRE'
            print(f"      {i}. <td>{valor}</td>  <!-- {nombre_col} -->")
    
    # 5. Verificar longitud de filas
    print(f"\n4️⃣ VERIFICACIÓN DE INTEGRIDAD...")
    
    if datos:
        primera_fila = datos[0]
        num_columnas_esperadas = len(columnas_data)
        num_columnas_en_datos = len(primera_fila)
        
        print(f"   📊 Columnas esperadas: {num_columnas_esperadas}")
        print(f"   📊 Columnas en datos: {num_columnas_en_datos}")
        
        if num_columnas_esperadas == num_columnas_en_datos:
            print(f"   ✅ INTEGRIDAD CORRECTA")
        else:
            print(f"   ❌ DISCREPANCIA EN NÚMERO DE COLUMNAS")
        
        # Verificar si todas las columnas esperadas están en los datos
        print(f"\n   🔍 VERIFICACIÓN COLUMNA POR COLUMNA:")
        for i, col in enumerate(columnas_data, 1):
            if col in primera_fila:
                valor = primera_fila[col]
                print(f"      {i}. ✅ {col}: {valor}")
            else:
                print(f"      {i}. ❌ {col}: NO ENCONTRADO EN DATOS")
        
        # Verificar si hay columnas extra en los datos
        columnas_extra = []
        for col in primera_fila:
            if col not in columnas_data:
                columnas_extra.append(col)
        
        if columnas_extra:
            print(f"\n   ⚠️  COLUMNAS EXTRA EN DATOS (no en columnas_data):")
            for col in columnas_extra:
                print(f"      - {col}: {primera_fila[col]}")
        else:
            print(f"\n   ✅ NO HAY COLUMNAS EXTRA")
    
    # 6. Simular la tabla HTML completa que se vería en el navegador
    print(f"\n5️⃣ TABLA HTML RESULTANTE (como se ve en el navegador)...")
    
    print(f"   <table>")
    print(f"     <thead>")
    print(f"       <tr>")
    for nombre in nombres_columnas:
        print(f"         <th>{nombre}</th>")
    print(f"       </tr>")
    print(f"     </thead>")
    print(f"     <tbody>")
    
    for idx, registro in enumerate(datos[:3], 1):  # Solo primeros 3 para no saturar
        print(f"       <tr>  <!-- Fila {idx} -->")
        for col_key in columnas_data:
            valor = registro.get(col_key, 'NO ENCONTRADO')
            print(f"         <td>{valor}</td>")
        print(f"       </tr>")
    
    if len(datos) > 3:
        print(f"       <!-- ... y {len(datos) - 3} filas más ... -->")
    
    print(f"     </tbody>")
    print(f"   </table>")
    
    print(f"\n6️⃣ RESUMEN FINAL...")
    print(f"   📊 Filas mostradas: {len(datos)}")
    print(f"   📋 Columnas mostradas: {len(nombres_columnas)}")
    print(f"   🔍 Columnas específicas verificadas:")
    
    if datos:
        primer_registro = datos[0]
        for col in ['mortalidad', 'causa_mortalidad', 'acciones_correctivas']:
            if col in primer_registro:
                posicion = columnas_data.index(col) + 1 if col in columnas_data else 'NO_EN_ORDEN'
                valor = primer_registro[col]
                nombre_display = format_column_name(col)
                print(f"      ✅ {nombre_display} (columna {posicion}): '{valor}'")
            else:
                print(f"      ❌ {col}: NO ENCONTRADO")

def format_column_name(col):
    """Formatear nombres de columnas igual que el frontend"""
    mappings = {
        '#': '#',
        'fecha': 'Fecha',
        'frecuencia_toma': 'Frecuencia Toma',
        'estanque_celda': 'Estanque/Celda',
        'referencia_alimento': 'Referencia Alimento',
        'cantidad_alimento': 'Cantidad Alimento',
        'mortalidad': 'Mortalidad',
        'causa_mortalidad': 'Causa Mortalidad',
        'acciones_correctivas': 'Acciones Correctivas'
    }
    return mappings.get(col, col.replace('_', ' ').title())

if __name__ == "__main__":
    simular_renderizado_frontend()
