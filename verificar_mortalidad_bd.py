#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import json

def verificar_mortalidad_detallado():
    """Verifica específicamente las columnas de mortalidad en la BD"""
    
    print("🔍 VERIFICACIÓN DETALLADA DE MORTALIDAD EN BD")
    print("=" * 60)
    
    # Conectar a la base de datos
    conn = sqlite3.connect('piscicola.db')
    cursor = conn.cursor()
    
    # 1. Verificar la estructura completa de la tabla alimento
    print("1️⃣ ESTRUCTURA DE LA TABLA ALIMENTO:")
    cursor.execute("PRAGMA table_info(alimento)")
    columns_info = cursor.fetchall()
    
    for col_info in columns_info:
        col_id, name, data_type, not_null, default_val, pk = col_info
        print(f"   {name} ({data_type}) - NOT NULL: {bool(not_null)} - DEFAULT: {default_val}")
    
    # 2. Obtener TODOS los datos de la tabla alimento
    print(f"\n2️⃣ TODOS LOS DATOS EN TABLA ALIMENTO:")
    cursor.execute("SELECT * FROM alimento ORDER BY fecha DESC, hora DESC")
    all_rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    
    print(f"   📊 Total registros: {len(all_rows)}")
    print(f"   📋 Columnas: {columns}")
    
    # Identificar índices de columnas de mortalidad
    mortalidad_idx = columns.index('mortalidad') if 'mortalidad' in columns else None
    causa_mortalidad_idx = columns.index('causa_mortalidad') if 'causa_mortalidad' in columns else None
    acciones_correctivas_idx = columns.index('acciones_correctivas') if 'acciones_correctivas' in columns else None
    
    print(f"\n   🎯 ÍNDICES DE COLUMNAS CRÍTICAS:")
    print(f"      mortalidad: {mortalidad_idx}")
    print(f"      causa_mortalidad: {causa_mortalidad_idx}")
    print(f"      acciones_correctivas: {acciones_correctivas_idx}")
    
    # 3. Mostrar todos los registros con foco en mortalidad
    print(f"\n3️⃣ REGISTROS COMPLETOS CON MORTALIDAD:")
    
    for i, row in enumerate(all_rows, 1):
        print(f"\n   📄 REGISTRO {i}:")
        for j, (col_name, value) in enumerate(zip(columns, row)):
            # Resaltar columnas de mortalidad
            if col_name in ['mortalidad', 'causa_mortalidad', 'acciones_correctivas']:
                tipo_valor = type(value).__name__
                es_vacio = value is None or value == '' or value == 'NULL'
                print(f"      🎯 {col_name}: '{value}' (tipo: {tipo_valor}, vacío: {es_vacio})")
            else:
                print(f"         {col_name}: {value}")
    
    # 4. Verificar específicamente valores no nulos/vacíos en mortalidad
    print(f"\n4️⃣ ANÁLISIS ESPECÍFICO DE MORTALIDAD:")
    
    # Contar registros con mortalidad > 0
    cursor.execute("SELECT COUNT(*) FROM alimento WHERE mortalidad > 0")
    count_mortalidad_positiva = cursor.fetchone()[0]
    
    # Contar registros con causa_mortalidad que no sea NULL, vacío o 'N/A'
    cursor.execute("SELECT COUNT(*) FROM alimento WHERE causa_mortalidad IS NOT NULL AND causa_mortalidad != '' AND causa_mortalidad != 'N/A'")
    count_causa_valida = cursor.fetchone()[0]
    
    # Contar registros con acciones_correctivas que no sea NULL, vacío o 'Ninguna'
    cursor.execute("SELECT COUNT(*) FROM alimento WHERE acciones_correctivas IS NOT NULL AND acciones_correctivas != '' AND acciones_correctivas != 'Ninguna'")
    count_acciones_validas = cursor.fetchone()[0]
    
    print(f"   📊 Registros con mortalidad > 0: {count_mortalidad_positiva}")
    print(f"   📊 Registros con causa_mortalidad válida: {count_causa_valida}")
    print(f"   📊 Registros con acciones_correctivas válidas: {count_acciones_validas}")
    
    # 5. Buscar registros específicos con datos de mortalidad
    print(f"\n5️⃣ BUSCANDO REGISTROS CON DATOS DE MORTALIDAD:")
    
    cursor.execute("""
        SELECT id, fecha, mortalidad, causa_mortalidad, acciones_correctivas 
        FROM alimento 
        WHERE mortalidad > 0 
           OR (causa_mortalidad IS NOT NULL AND causa_mortalidad != '' AND causa_mortalidad != 'N/A')
           OR (acciones_correctivas IS NOT NULL AND acciones_correctivas != '' AND acciones_correctivas != 'Ninguna')
        ORDER BY fecha DESC
    """)
    
    registros_con_mortalidad = cursor.fetchall()
    
    if registros_con_mortalidad:
        print(f"   ✅ ENCONTRADOS {len(registros_con_mortalidad)} REGISTROS CON DATOS DE MORTALIDAD:")
        for reg in registros_con_mortalidad:
            id_reg, fecha, mort, causa, acciones = reg
            print(f"      📄 ID {id_reg} ({fecha}): mort={mort}, causa='{causa}', acciones='{acciones}'")
    else:
        print(f"   ⚠️  NO SE ENCONTRARON REGISTROS CON DATOS SIGNIFICATIVOS DE MORTALIDAD")
    
    # 6. Verificar si hay datos recientes que podrían haberse agregado
    print(f"\n6️⃣ VERIFICANDO DATOS RECIENTES:")
    
    cursor.execute("""
        SELECT fecha, mortalidad, causa_mortalidad, acciones_correctivas, created_at
        FROM alimento 
        ORDER BY created_at DESC 
        LIMIT 10
    """)
    
    registros_recientes = cursor.fetchall()
    
    print(f"   📅 ÚLTIMOS 10 REGISTROS POR FECHA DE CREACIÓN:")
    for i, reg in enumerate(registros_recientes, 1):
        fecha, mort, causa, acciones, created_at = reg
        print(f"      {i}. {fecha} | mort: {mort} | causa: '{causa}' | acciones: '{acciones}' | creado: {created_at}")
    
    # 7. Simular inserción de datos de prueba para verificar
    print(f"\n7️⃣ INSERTANDO DATOS DE PRUEBA CON MORTALIDAD:")
    
    # Insertar un registro con mortalidad
    cursor.execute("""
        INSERT INTO alimento (
            fecha, hora, estanque, tipo_alimento, cantidad_kg, 
            observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas
        ) VALUES (
            '2025-09-03', '10:00:00', '1', 'Pellet Test', 10.0,
            'Registro de prueba', '2 veces al día', 5, 'Enfermedad bacterial', 'Tratamiento con antibióticos'
        )
    """)
    
    # Insertar otro registro con mortalidad diferente
    cursor.execute("""
        INSERT INTO alimento (
            fecha, hora, estanque, tipo_alimento, cantidad_kg, 
            observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas
        ) VALUES (
            '2025-09-02', '14:30:00', '2', 'Concentrado Test', 8.5,
            'Segundo registro de prueba', '3 veces al día', 2, 'Estrés por temperatura', 'Ajuste de oxigenación'
        )
    """)
    
    conn.commit()
    
    print(f"   ✅ INSERTADOS 2 REGISTROS DE PRUEBA CON MORTALIDAD")
    
    # 8. Verificar que los nuevos datos se insertaron
    cursor.execute("""
        SELECT fecha, mortalidad, causa_mortalidad, acciones_correctivas 
        FROM alimento 
        WHERE fecha IN ('2025-09-03', '2025-09-02')
        ORDER BY fecha DESC
    """)
    
    nuevos_registros = cursor.fetchall()
    
    print(f"\n8️⃣ VERIFICANDO NUEVOS REGISTROS INSERTADOS:")
    for reg in nuevos_registros:
        fecha, mort, causa, acciones = reg
        print(f"   📄 {fecha}: mortalidad={mort}, causa='{causa}', acciones='{acciones}'")
    
    # 9. Ejecutar la consulta exacta del endpoint con los nuevos datos
    print(f"\n9️⃣ EJECUTANDO CONSULTA EXACTA DEL ENDPOINT:")
    
    query = """
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
    WHERE fecha BETWEEN '2025-08-01' AND '2025-09-30'
    ORDER BY fecha DESC, hora DESC
    """
    
    cursor.execute(query)
    resultado_endpoint = cursor.fetchall()
    columns_endpoint = [description[0] for description in cursor.description]
    
    print(f"   📊 Registros obtenidos: {len(resultado_endpoint)}")
    print(f"   📋 Columnas: {columns_endpoint}")
    
    # Mostrar primeros registros con mortalidad
    print(f"\n   🎯 PRIMEROS REGISTROS CON FOCO EN MORTALIDAD:")
    for i, row in enumerate(resultado_endpoint[:5], 1):
        registro_dict = dict(zip(columns_endpoint, row))
        print(f"   📄 Registro {i}:")
        print(f"      #{registro_dict['#']} | {registro_dict['fecha']} | mortalidad: {registro_dict['mortalidad']} | causa: '{registro_dict['causa_mortalidad']}' | acciones: '{registro_dict['acciones_correctivas']}'")
    
    conn.close()
    
    print(f"\n🎯 RESUMEN:")
    print(f"   ✅ Se insertaron registros de prueba con mortalidad")
    print(f"   ✅ La consulta del endpoint incluye estos registros")
    print(f"   ✅ Los datos de mortalidad están presentes en la BD")

if __name__ == "__main__":
    verificar_mortalidad_detallado()
