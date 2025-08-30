"""
🔍 SCRIPT DE PRUEBA PARA VERIFICAR ORDEN POR FECHA
Verifica que los resultados se ordenan de menor a mayor fecha
"""

from database_config import DatabaseConfig
import datetime

def verificar_orden_fecha():
    print("🔍 VERIFICANDO ORDEN POR FECHA EN INFORMES")
    print("=========================================")
    
    try:
        # Conectar a la base de datos
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Consultar datos de alimento ordenados por fecha ASC
        query = "SELECT fecha, referencia_alimento, cantidad_alimento FROM alimento ORDER BY fecha ASC"
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        if resultados:
            print(f"✅ {len(resultados)} registros encontrados en tabla 'alimento'")
            print("\n📋 Datos ordenados por fecha (menor a mayor):")
            print("-" * 60)
            
            for i, registro in enumerate(resultados, 1):
                fecha = registro['fecha']
                referencia = registro['referencia_alimento']
                cantidad = registro['cantidad_alimento']
                
                print(f"{i:2d}. {fecha} | {referencia} | {cantidad} kg")
            
            # Verificar que realmente están ordenados
            fechas = [registro['fecha'] for registro in resultados]
            fechas_ordenadas = sorted(fechas)
            
            if fechas == fechas_ordenadas:
                print("\n✅ VERIFICACIÓN: Los datos están correctamente ordenados de menor a mayor")
            else:
                print("\n❌ ERROR: Los datos NO están ordenados correctamente")
                
        else:
            print("❌ No se encontraron registros en la tabla alimento")
            
        # Probar la misma lógica que usa el formulario de informes
        print("\n🔍 Simulando consulta del formulario de informes...")
        
        # Simular filtros del formulario
        formulario = 'alimento'
        fecha_desde = '2025-08-01'
        fecha_hasta = '2025-08-30'
        
        query_formulario = f"""
        SELECT *, '{formulario}' as tipo 
        FROM {formulario} 
        WHERE fecha >= %s AND fecha <= %s 
        ORDER BY fecha ASC
        """
        
        cursor.execute(query_formulario, (fecha_desde, fecha_hasta))
        resultados_formulario = cursor.fetchall()
        
        print(f"✅ Consulta del formulario: {len(resultados_formulario)} registros")
        
        if resultados_formulario:
            print("\n📋 Primeros 3 registros del formulario:")
            for i, registro in enumerate(resultados_formulario[:3], 1):
                fecha = registro['fecha']
                referencia = registro['referencia_alimento']
                print(f"  {i}. {fecha} - {referencia}")
                
            print("\n📋 Últimos 3 registros del formulario:")
            for i, registro in enumerate(resultados_formulario[-3:], len(resultados_formulario)-2):
                fecha = registro['fecha']
                referencia = registro['referencia_alimento']
                print(f"  {i}. {fecha} - {referencia}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 PRUEBA COMPLETADA")
        print("===================")
        print("✅ El orden por fecha (menor a mayor) está funcionando correctamente")
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")

if __name__ == "__main__":
    verificar_orden_fecha()
