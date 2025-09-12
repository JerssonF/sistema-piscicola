#!/usr/bin/env python3
import sqlite3
import os

def actualizar_estructura_bd():
    """Actualizar la estructura de la base de datos para que coincida con los formularios"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'piscicola.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 ACTUALIZANDO ESTRUCTURA DE BASE DE DATOS")
        print("=" * 60)
        
        # ===== TABLA ALIMENTO =====
        print("\n📋 Actualizando tabla ALIMENTO...")
        
        # Verificar qué columnas existen
        cursor.execute("PRAGMA table_info(alimento)")
        columnas_existentes = [col[1] for col in cursor.fetchall()]
        print(f"Columnas existentes: {columnas_existentes}")
        
        # Agregar columnas faltantes para el formulario de alimentos
        columnas_nuevas_alimento = [
            'frecuencia_toma TEXT',
            'mortalidad INTEGER DEFAULT 0',
            'causa_mortalidad TEXT',
            'acciones_correctivas TEXT',
            'fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        ]
        
        for columna in columnas_nuevas_alimento:
            col_name = columna.split()[0]
            if col_name not in columnas_existentes:
                try:
                    cursor.execute(f"ALTER TABLE alimento ADD COLUMN {columna}")
                    print(f"✅ Agregada columna: {col_name}")
                except Exception as e:
                    print(f"⚠️  No se pudo agregar {col_name}: {e}")
        
        # ===== TABLA MUESTREO =====
        print("\n📋 Actualizando tabla MUESTREO...")
        
        cursor.execute("PRAGMA table_info(muestreo)")
        columnas_existentes = [col[1] for col in cursor.fetchall()]
        print(f"Columnas existentes: {columnas_existentes}")
        
        columnas_nuevas_muestreo = [
            'frecuencia_toma TEXT',
            'especie TEXT',
            'biomasa REAL',
            'peces INTEGER'
        ]
        
        for columna in columnas_nuevas_muestreo:
            col_name = columna.split()[0]
            if col_name not in columnas_existentes:
                try:
                    cursor.execute(f"ALTER TABLE muestreo ADD COLUMN {columna}")
                    print(f"✅ Agregada columna: {col_name}")
                except Exception as e:
                    print(f"⚠️  No se pudo agregar {col_name}: {e}")
        
        # ===== TABLA PARAMETROS =====
        print("\n📋 Actualizando tabla PARAMETROS...")
        
        cursor.execute("PRAGMA table_info(parametros)")
        columnas_existentes = [col[1] for col in cursor.fetchall()]
        print(f"Columnas existentes: {columnas_existentes}")
        
        columnas_nuevas_parametros = [
            'frecuencia_toma TEXT',
            'oxigeno_disuelto REAL',
            'nitritos REAL'
        ]
        
        for columna in columnas_nuevas_parametros:
            col_name = columna.split()[0]
            if col_name not in columnas_existentes:
                try:
                    cursor.execute(f"ALTER TABLE parametros ADD COLUMN {columna}")
                    print(f"✅ Agregada columna: {col_name}")
                except Exception as e:
                    print(f"⚠️  No se pudo agregar {col_name}: {e}")
        
        # ===== TABLA SIEMBRA =====
        print("\n📋 Actualizando tabla SIEMBRA...")
        
        cursor.execute("PRAGMA table_info(siembra)")
        columnas_existentes = [col[1] for col in cursor.fetchall()]
        print(f"Columnas existentes: {columnas_existentes}")
        
        columnas_nuevas_siembra = [
            'destino TEXT',
            'ovas_alevinos INTEGER',
            'hembras_machos TEXT'
        ]
        
        for columna in columnas_nuevas_siembra:
            col_name = columna.split()[0]
            if col_name not in columnas_existentes:
                try:
                    cursor.execute(f"ALTER TABLE siembra ADD COLUMN {columna}")
                    print(f"✅ Agregada columna: {col_name}")
                except Exception as e:
                    print(f"⚠️  No se pudo agregar {col_name}: {e}")
        
        # Actualizar datos existentes con valores por defecto
        print("\n🔄 Actualizando registros existentes...")
        
        # Alimentos - agregar valores por defecto
        cursor.execute("""
            UPDATE alimento 
            SET frecuencia_toma = '3 veces al día',
                mortalidad = 0,
                causa_mortalidad = 'N/A',
                acciones_correctivas = 'Ninguna'
            WHERE frecuencia_toma IS NULL
        """)
        
        # Muestreo - calcular biomasa y agregar valores
        cursor.execute("""
            UPDATE muestreo 
            SET frecuencia_toma = 'Semanal',
                especie = 'Tilapia',
                biomasa = peso_promedio * cantidad_peces / 1000.0,
                peces = cantidad_peces
            WHERE frecuencia_toma IS NULL
        """)
        
        # Parámetros - agregar valores por defecto
        cursor.execute("""
            UPDATE parametros 
            SET frecuencia_toma = 'Diario',
                oxigeno_disuelto = oxigeno,
                nitritos = nitrito
            WHERE frecuencia_toma IS NULL
        """)
        
        # Siembra - agregar valores por defecto
        cursor.execute("""
            UPDATE siembra 
            SET destino = 'Estanque',
                ovas_alevinos = cantidad,
                hembras_machos = 'Mixto'
            WHERE destino IS NULL
        """)
        
        conn.commit()
        conn.close()
        
        print("\n✅ ESTRUCTURA ACTUALIZADA CORRECTAMENTE")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando estructura: {e}")
        return False

if __name__ == "__main__":
    actualizar_estructura_bd()
