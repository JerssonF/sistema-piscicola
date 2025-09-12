#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Verificación del esquema completo de la base de datos SQLite
Comparando con lo que el usuario ve en phpMyAdmin
"""

import sqlite3
import json
from collections import OrderedDict

# Conectar a la base de datos
conn = sqlite3.connect('piscicola.db')
cursor = conn.cursor()

print("🔍 VERIFICACIÓN DEL ESQUEMA COMPLETO DE SQLITE")
print("=" * 60)

# Verificar todas las tablas disponibles
print("\n1️⃣ LISTANDO TODAS LAS TABLAS EN LA BASE DE DATOS:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()
for tabla in tablas:
    print(f"   📋 {tabla[0]}")

print("\n2️⃣ ANALIZANDO ESTRUCTURA DE CADA TABLA:")

for tabla in tablas:
    nombre_tabla = tabla[0]
    print(f"\n📊 TABLA: {nombre_tabla}")
    print("-" * 40)
    
    # Obtener información del esquema
    cursor.execute(f"PRAGMA table_info({nombre_tabla});")
    esquema = cursor.fetchall()
    
    print(f"   📋 COLUMNAS EN {nombre_tabla}:")
    for i, col in enumerate(esquema, 1):
        col_id, nombre, tipo, not_null, default, pk = col
        print(f"      {i:2d}. {nombre:20} | Tipo: {tipo:10} | Not Null: {not_null} | Default: {default} | PK: {pk}")
    
    # Contar registros
    cursor.execute(f"SELECT COUNT(*) FROM {nombre_tabla};")
    total = cursor.fetchone()[0]
    print(f"   📊 TOTAL DE REGISTROS: {total}")
    
    # Mostrar los primeros 3 registros para verificar contenido
    if total > 0:
        cursor.execute(f"SELECT * FROM {nombre_tabla} LIMIT 3;")
        registros = cursor.fetchall()
        nombres_columnas = [desc[0] for desc in cursor.description]
        
        print(f"   📄 PRIMEROS 3 REGISTROS:")
        for i, registro in enumerate(registros, 1):
            print(f"      Registro {i}:")
            for j, valor in enumerate(registro):
                print(f"         {nombres_columnas[j]}: {valor}")

print("\n3️⃣ CONSULTA SQL ESPECÍFICA PARA TABLA 'alimento':")
print("-" * 50)

# Ejecutar la misma consulta que usa el endpoint
cursor.execute("SELECT * FROM alimento ORDER BY fecha DESC;")
registros = cursor.fetchall()
nombres_columnas = [desc[0] for desc in cursor.description]

print(f"📋 COLUMNAS RETORNADAS POR SELECT * FROM alimento:")
for i, col in enumerate(nombres_columnas, 1):
    print(f"   {i:2d}. {col}")

print(f"\n📊 TOTAL DE REGISTROS RETORNADOS: {len(registros)}")

print(f"\n📄 PRIMER REGISTRO COMPLETO:")
if registros:
    primer_registro = registros[0]
    for i, valor in enumerate(primer_registro):
        print(f"   {nombres_columnas[i]:25}: {valor}")

# Verificar si hay índices o vistas
print("\n4️⃣ VERIFICANDO ÍNDICES Y VISTAS:")
print("-" * 40)

cursor.execute("SELECT name, type, sql FROM sqlite_master WHERE type IN ('index', 'view');")
otros_objetos = cursor.fetchall()

if otros_objetos:
    for obj in otros_objetos:
        nombre, tipo, sql = obj
        print(f"   {tipo.upper()}: {nombre}")
        if sql:
            print(f"      SQL: {sql}")
else:
    print("   ℹ️ No se encontraron índices o vistas adicionales")

# Cerrar conexión
conn.close()

print("\n✅ VERIFICACIÓN COMPLETA")
print("=" * 60)
print("\n💡 NOTA: Si phpMyAdmin muestra más columnas, podría ser:")
print("   1. Columnas virtuales o calculadas")
print("   2. Metadatos adicionales de phpMyAdmin")
print("   3. Diferente estructura en otra base de datos")
print("   4. Vistas o consultas complejas en phpMyAdmin")
