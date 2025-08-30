#!/usr/bin/env python3
"""
Test directo de ORDER BY en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_config import get_connection

def test_orden_fechas():
    """Prueba el ORDER BY directamente en la BD"""
    
    try:
        # Conectar a la base de datos
        connection = get_connection()
        
        if not connection:
            print("❌ No se pudo conectar a la base de datos")
            return
            
        cursor = connection.cursor()
        
        # Query con ORDER BY fecha ASC
        query = "SELECT fecha, estanque, peso, talla FROM muestreo ORDER BY fecha ASC LIMIT 10"
        
        print(f"🔍 Ejecutando: {query}")
        cursor.execute(query)
        
        resultados = cursor.fetchall()
        
        print("\n📅 Resultados ordenados por fecha (ASC - menor a mayor):")
        print("=" * 60)
        
        for fila in resultados:
            fecha, estanque, peso, talla = fila
            print(f"Fecha: {fecha} | Estanque: {estanque} | Peso: {peso} | Talla: {talla}")
        
        # Cerrar conexiones
        cursor.close()
        connection.close()
        
        print("\n✅ Test completado")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Probando ORDER BY en la base de datos...")
    test_orden_fechas()
