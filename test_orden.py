import mysql.connector

try:
    # Conexión directa
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='piscicola'
    )
    
    cursor = conn.cursor()
    
    # Verificar datos ordenados
    cursor.execute("SELECT fecha, referencia_alimento FROM alimento ORDER BY fecha ASC")
    resultados = cursor.fetchall()
    
    print("Datos ordenados por fecha (menor a mayor):")
    for i, (fecha, ref) in enumerate(resultados, 1):
        print(f"{i}. {fecha} - {ref}")
    
    cursor.close()
    conn.close()
    print("✅ Orden verificado correctamente")
    
except Exception as e:
    print(f"Error: {e}")
