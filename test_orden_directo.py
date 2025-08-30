"""
🔍 PRUEBA DIRECTA DE ORDEN EN BASE DE DATOS
"""

import mysql.connector
from datetime import datetime

def probar_orden_directo():
    print("🔍 PROBANDO ORDEN DE FECHAS DIRECTAMENTE")
    print("=" * 45)
    
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='piscicola'
        )
        
        cursor = conn.cursor()
        
        # Prueba 1: Orden ASC (menor a mayor)
        print("\n📊 ORDEN ASC (menor a mayor) - DESEADO:")
        print("-" * 45)
        cursor.execute("SELECT fecha, referencia_alimento FROM alimento ORDER BY fecha ASC LIMIT 10")
        resultados_asc = cursor.fetchall()
        
        for i, (fecha, ref) in enumerate(resultados_asc, 1):
            print(f"{i:2d}. {fecha} - {ref}")
        
        # Prueba 2: Orden DESC (mayor a menor) 
        print("\n📊 ORDEN DESC (mayor a menor) - NO DESEADO:")
        print("-" * 45)
        cursor.execute("SELECT fecha, referencia_alimento FROM alimento ORDER BY fecha DESC LIMIT 10")
        resultados_desc = cursor.fetchall()
        
        for i, (fecha, ref) in enumerate(resultados_desc, 1):
            print(f"{i:2d}. {fecha} - {ref}")
        
        # Verificar qué orden está usando actualmente el sistema
        print("\n🔍 SIMULANDO CONSULTA DEL FORMULARIO:")
        print("-" * 45)
        
        # Esta es la consulta exacta que usa el formulario
        query = """
        SELECT *, 'alimento' as tipo 
        FROM alimento 
        WHERE fecha >= %s AND fecha <= %s 
        ORDER BY fecha ASC
        """
        
        cursor.execute(query, ('2025-08-01', '2025-08-31'))
        resultados_formulario = cursor.fetchall()
        
        print(f"Registros encontrados: {len(resultados_formulario)}")
        
        for i, registro in enumerate(resultados_formulario[:5], 1):
            fecha = registro[0]  # Primer campo es fecha
            print(f"{i:2d}. {fecha}")
        
        if len(resultados_formulario) > 5:
            print("...")
            for i, registro in enumerate(resultados_formulario[-3:], len(resultados_formulario)-2):
                fecha = registro[0]
                print(f"{i:2d}. {fecha}")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Prueba completada")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    probar_orden_directo()
