#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que las tablas funcionan correctamente
"""

import mysql.connector
from mysql.connector import Error
from datetime import date, time

def test_database_tables():
    """Probar inserción en todas las tablas"""
    
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'piscicola'
    }
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("🧪 Probando inserción en todas las tablas...\n")
        
        # Test tabla alimento
        print("1️⃣ Probando tabla 'alimento'...")
        cursor.execute("""
            INSERT INTO alimento (
                fecha, frecuencia_toma, estanque_celda, referencia_alimento,
                cantidad_alimento, mortalidad, causa_mortalidad, acciones_correctivas
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            date.today(), "2 veces al día", "Estanque A1", "Alimento Premium",
            25.5, 2, "Estrés por temperatura", "Ajustar temperatura del agua"
        ))
        print("✅ Inserción en 'alimento' exitosa")
        
        # Test tabla ingreso_alimentos
        print("\n2️⃣ Probando tabla 'ingreso_alimentos'...")
        cursor.execute("""
            INSERT INTO ingreso_alimentos (
                fecha, hora, ingreso_comida, cantidad, transporte, observaciones
            ) VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            date.today(), time(8, 30), "Concentrado 24%", 50.0, "Camión refrigerado", "Entrega en buen estado"
        ))
        print("✅ Inserción en 'ingreso_alimentos' exitosa")
        
        # Test tabla muestreo
        print("\n3️⃣ Probando tabla 'muestreo'...")
        cursor.execute("""
            INSERT INTO muestreo (
                fecha, frecuencia_toma, especie, biomasa,
                estanque_celda, peces, peso_promedio_g,
                promedio_total_g, acciones_correctivas
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            date.today(), "Semanal", "Tilapia", 150.75,
            "Estanque B2", 100, 125.5, 12550.0, "Continuar alimentación normal"
        ))
        print("✅ Inserción en 'muestreo' exitosa")
        
        # Confirmar cambios
        connection.commit()
        
        # Verificar datos insertados
        print("\n📊 Verificando datos insertados:")
        
        cursor.execute("SELECT COUNT(*) FROM alimento")
        count_alimento = cursor.fetchone()[0]
        print(f"   - Registros en 'alimento': {count_alimento}")
        
        cursor.execute("SELECT COUNT(*) FROM ingreso_alimentos")
        count_ingreso = cursor.fetchone()[0]
        print(f"   - Registros en 'ingreso_alimentos': {count_ingreso}")
        
        cursor.execute("SELECT COUNT(*) FROM muestreo")
        count_muestreo = cursor.fetchone()[0]
        print(f"   - Registros en 'muestreo': {count_muestreo}")
        
        print("\n🎉 ¡Todas las tablas funcionan correctamente!")
        print("✨ La base de datos está lista para la aplicación Flask")
        
    except Error as e:
        print(f"❌ Error en la prueba: {e}")
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    test_database_tables()
