import mysql.connector

# Conectar a la base de datos
try:
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='piscicola'
    )
    
    cursor = conn.cursor()
    
    print("📅 VERIFICANDO ORDEN DE FECHAS (DEBE SER MENOR A MAYOR)")
    print("=" * 55)
    
    # Consulta igual a la del formulario de informes
    query = "SELECT fecha, referencia_alimento FROM alimento ORDER BY fecha ASC LIMIT 10"
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    print("Fechas ordenadas de MENOR a MAYOR (más antigua primero):")
    print("-" * 55)
    
    for i, (fecha, referencia) in enumerate(resultados, 1):
        print(f"{i:2d}. {fecha} - {referencia}")
    
    cursor.close()
    conn.close()
    
    print("\n✅ Si las fechas van de menor a mayor, el orden está correcto!")
    
except Exception as e:
    print(f"❌ Error: {e}")
