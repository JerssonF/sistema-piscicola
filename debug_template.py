import mysql.connector
from datetime import datetime

def test_query():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='piscicola'
        )
        
        cursor = conn.cursor(dictionary=True)
        query = "SELECT *, 'alimento' as tipo FROM alimento WHERE fecha >= %s AND fecha <= %s ORDER BY fecha DESC"
        params = ['2025-08-01', '2025-08-26']
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        print(f"✅ ENCONTRADOS {len(resultados)} registros")
        print("=" * 50)
        
        for i, registro in enumerate(resultados, 1):
            print(f"REGISTRO {i}:")
            for key, value in registro.items():
                print(f"  {key}: {value}")
            print("-" * 30)
            
        # Simular lo que ve el template
        formulario_seleccionado = 'alimento'
        print(f"\nformulario_seleccionado = '{formulario_seleccionado}'")
        print(f"Condición: formulario_seleccionado == 'alimento' -> {formulario_seleccionado == 'alimento'}")
        
        if len(resultados) > 0:
            registro = resultados[0]
            print(f"\nPRIMER REGISTRO PROCESADO:")
            print(f"  fecha: {registro['fecha'].strftime('%d/%m/%Y') if registro['fecha'] else 'N/A'}")
            print(f"  frecuencia_toma: {registro['frecuencia_toma'] or 'N/A'}")
            print(f"  estanque_celda: {registro['estanque_celda'] or 'N/A'}")
            print(f"  referencia_alimento: {registro['referencia_alimento'] or 'N/A'}")
            print(f"  cantidad_alimento: {'{:.2f}'.format(registro['cantidad_alimento']) if registro['cantidad_alimento'] else '0.00'}")
            print(f"  mortalidad: {registro['mortalidad'] or '0'}")
            print(f"  causa_mortalidad: {registro['causa_mortalidad'] or 'N/A'}")
            print(f"  acciones_correctivas: {registro['acciones_correctivas'] or 'N/A'}")
            
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    test_query()
