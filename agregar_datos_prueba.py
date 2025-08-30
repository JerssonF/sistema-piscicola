"""
📊 AGREGAR DATOS DE PRUEBA CON DIFERENTES FECHAS
Para verificar el orden de menor a mayor en informes
"""

import mysql.connector
from datetime import datetime, timedelta

def agregar_datos_prueba():
    print("📊 AGREGANDO DATOS DE PRUEBA CON DIFERENTES FECHAS")
    print("=================================================")
    
    try:
        # Conexión a la base de datos
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='piscicola'
        )
        
        cursor = conn.cursor()
        
        # Datos de prueba con diferentes fechas
        datos_prueba = [
            ('2025-08-15', '08:00', 'Estanque-1', 'Alimento Premium A', 15.5, 0),
            ('2025-08-10', '09:00', 'Estanque-2', 'Alimento Premium B', 12.0, 0),
            ('2025-08-25', '10:00', 'Estanque-1', 'Alimento Premium C', 18.0, 1),
            ('2025-08-05', '11:00', 'Estanque-3', 'Alimento Premium D', 20.5, 0),
            ('2025-08-30', '12:00', 'Estanque-2', 'Alimento Premium E', 14.5, 0),
            ('2025-08-01', '13:00', 'Estanque-1', 'Alimento Premium F', 16.0, 0)
        ]
        
        # Insertar datos de prueba
        query = """
        INSERT INTO alimento (fecha, frecuencia_toma, estanque_celda, referencia_alimento, cantidad_alimento, mortalidad)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        print("📋 Insertando datos de prueba...")
        for i, datos in enumerate(datos_prueba, 1):
            try:
                cursor.execute(query, datos)
                print(f"  ✅ {i}. Fecha: {datos[0]} - Alimento: {datos[3]}")
            except Exception as e:
                print(f"  ⚠️ {i}. Error insertando {datos[0]}: {e}")
        
        conn.commit()
        
        # Verificar datos insertados ordenados por fecha
        print("\n📋 Verificando orden de fechas (menor a mayor):")
        cursor.execute("SELECT fecha, referencia_alimento FROM alimento ORDER BY fecha ASC")
        resultados = cursor.fetchall()
        
        for i, (fecha, referencia) in enumerate(resultados, 1):
            print(f"  {i:2d}. {fecha} - {referencia}")
        
        print(f"\n✅ Total de registros: {len(resultados)}")
        print("✅ Datos de prueba agregados exitosamente")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    agregar_datos_prueba()
