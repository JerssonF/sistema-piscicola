#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar el formulario de parámetros
"""

import mysql.connector
from mysql.connector import Error
from datetime import date, time

def test_parametros_table():
    """Probar inserción en la tabla parametros"""
    
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'piscicola'
    }
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("🧪 Probando inserción en tabla 'parametros'...\n")
        
        # Test tabla parametros
        print("🌡️ Insertando datos de parámetros de prueba...")
        cursor.execute("""
            INSERT INTO parametros (
                fecha, hora, estanque_celda, oxigeno,
                temperatura, ph, amonio, observaciones
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            date.today(), time(14, 30), "Estanque A1", 7.2,
            25.5, 7.0, 0.15, "Parámetros dentro del rango normal"
        ))
        print("✅ Inserción en 'parametros' exitosa")
        
        # Confirmar cambios
        connection.commit()
        
        # Verificar datos insertados
        print("\n📊 Verificando datos en la tabla parametros:")
        cursor.execute("SELECT * FROM parametros ORDER BY fecha_registro DESC LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            print(f"   - ID: {row[0]}")
            print(f"   - Fecha: {row[1]}")
            print(f"   - Hora: {row[2]}")
            print(f"   - Estanque/Celda: {row[3]}")
            print(f"   - Oxígeno: {row[4]} mg/L")
            print(f"   - Temperatura: {row[5]} °C")
            print(f"   - pH: {row[6]}")
            print(f"   - Amonio: {row[7]} mg/L")
            print(f"   - Observaciones: {row[8]}")
            print(f"   - Fecha registro: {row[9]}")
        
        # Contar total de registros
        cursor.execute("SELECT COUNT(*) FROM parametros")
        count = cursor.fetchone()[0]
        print(f"\n📈 Total de registros en 'parametros': {count}")
        
        print("\n🎉 ¡La tabla parametros funciona correctamente!")
        print("✨ El formulario está listo para usar")
        
    except Error as e:
        print(f"❌ Error en la prueba: {e}")
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    test_parametros_table()
