#!/usr/bin/env python3
"""
Test directo del ORDER BY en la tabla alimento
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_config import get_connection
from datetime import datetime

def test_orden_alimento():
    """Prueba directa en la tabla alimento"""
    
    try:
        # Conectar a la base de datos
        connection = get_connection()
        
        if not connection:
            print("❌ No se pudo conectar a la base de datos")
            return
            
        cursor = connection.cursor(dictionary=True)
        
        # Query exacta que debería usar la aplicación
        query = """
        SELECT fecha, referencia_alimento, cantidad_alimento, estanque_celda
        FROM alimento 
        WHERE fecha >= %s AND fecha <= %s
        ORDER BY fecha ASC
        """
        
        params = ['2025-08-01', '2025-08-30']
        
        print(f"🔍 Ejecutando: {query}")
        print(f"🔍 Parámetros: {params}")
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        print(f"\n📅 Resultados ordenados por fecha ASC (menor a mayor):")
        print("=" * 70)
        
        for i, fila in enumerate(resultados, 1):
            fecha = fila['fecha']
            referencia = fila['referencia_alimento']
            cantidad = fila['cantidad_alimento']
            estanque = fila['estanque_celda']
            print(f"{i:2d}. {fecha} | {referencia:15s} | {cantidad:8s} | Estanque: {estanque}")
        
        print(f"\n📊 Total registros: {len(resultados)}")
        
        # Verificar si está ordenado correctamente
        fechas = [r['fecha'] for r in resultados]
        fechas_ordenadas = sorted(fechas)
        
        if fechas == fechas_ordenadas:
            print("✅ Las fechas están correctamente ordenadas (ASC)")
        else:
            print("❌ Las fechas NO están ordenadas correctamente")
            print("   Orden actual:", [str(f) for f in fechas])
            print("   Orden correcto:", [str(f) for f in fechas_ordenadas])
        
        # Cerrar conexiones
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Probando ORDER BY directamente en tabla alimento...")
    test_orden_alimento()
