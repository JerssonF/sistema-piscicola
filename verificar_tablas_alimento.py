#!/usr/bin/env python3
"""
Verificar contenido y estructura de las tablas alimento e ingreso_alimentos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_config import get_connection

def verificar_tablas():
    """Verificar ambas tablas de alimentos"""
    
    try:
        connection = get_connection()
        
        if not connection:
            print("❌ No se pudo conectar a la base de datos")
            return
            
        cursor = connection.cursor(dictionary=True)
        
        # Verificar tabla alimento
        print("🔍 TABLA: alimento")
        print("=" * 50)
        
        cursor.execute("SELECT fecha, referencia_alimento FROM alimento ORDER BY fecha ASC")
        alimento_resultados = cursor.fetchall()
        
        print(f"Total registros: {len(alimento_resultados)}")
        for i, row in enumerate(alimento_resultados, 1):
            print(f"  {i}. {row['fecha']} - {row['referencia_alimento']}")
        
        print("\n🔍 TABLA: ingreso_alimentos")
        print("=" * 50)
        
        cursor.execute("DESCRIBE ingreso_alimentos")
        estructura = cursor.fetchall()
        print("Estructura de la tabla:")
        for col in estructura:
            print(f"  - {col['Field']} ({col['Type']})")
        
        # Ver contenido
        cursor.execute("SELECT * FROM ingreso_alimentos ORDER BY fecha ASC")
        ingreso_resultados = cursor.fetchall()
        
        print(f"\nTotal registros: {len(ingreso_resultados)}")
        for i, row in enumerate(ingreso_resultados, 1):
            fecha = row.get('fecha', 'No fecha')
            print(f"  {i}. {fecha} - {row}")
        
        # Verificar rangos de fecha
        print("\n📅 VERIFICACIÓN DE FECHAS EN RANGO:")
        print("=" * 50)
        
        fecha_desde = '2025-08-01'
        fecha_hasta = '2025-08-30'
        
        # Tabla alimento
        cursor.execute("SELECT COUNT(*) as total FROM alimento WHERE fecha >= %s AND fecha <= %s", 
                      (fecha_desde, fecha_hasta))
        count_alimento = cursor.fetchone()['total']
        
        # Tabla ingreso_alimentos  
        cursor.execute("SELECT COUNT(*) as total FROM ingreso_alimentos WHERE fecha >= %s AND fecha <= %s", 
                      (fecha_desde, fecha_hasta))
        count_ingreso = cursor.fetchone()['total']
        
        print(f"Registros en 'alimento' (01-30/08/2025): {count_alimento}")
        print(f"Registros en 'ingreso_alimentos' (01-30/08/2025): {count_ingreso}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Verificando tablas de alimentos...")
    verificar_tablas()
