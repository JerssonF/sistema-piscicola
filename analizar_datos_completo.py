import sqlite3

def analizar_datos_alimento_completo():
    """Análisis completo de los datos de alimento y qué se muestra en la interfaz"""
    
    conn = sqlite3.connect('piscicola.db')
    cursor = conn.cursor()

    print("🔍 ANÁLISIS COMPLETO DE DATOS DE ALIMENTO")
    print("="*70)
    
    # 1. Verificar estructura de la tabla
    print("\n1️⃣ ESTRUCTURA DE LA TABLA ALIMENTO:")
    cursor.execute('PRAGMA table_info(alimento)')
    columns_info = cursor.fetchall()
    for col in columns_info:
        print(f"   {col[1]} ({col[2]}) - Null: {col[3] == 0}")
    
    # 2. Contar registros totales
    cursor.execute('SELECT COUNT(*) FROM alimento')
    total_registros = cursor.fetchone()[0]
    print(f"\n2️⃣ TOTAL DE REGISTROS: {total_registros}")
    
    # 3. Verificar datos de las columnas específicas
    print("\n3️⃣ VERIFICANDO DATOS EN COLUMNAS ESPECÍFICAS:")
    
    # Columnas que deberían aparecer en la interfaz
    columnas_interfaz = [
        'fecha', 'frecuencia_toma', 'estanque', 'tipo_alimento', 
        'cantidad_kg', 'mortalidad', 'causa_mortalidad', 'acciones_correctivas'
    ]
    
    for columna in columnas_interfaz:
        cursor.execute(f'SELECT COUNT(*) FROM alimento WHERE {columna} IS NOT NULL AND {columna} != ""')
        no_vacios = cursor.fetchone()[0]
        
        cursor.execute(f'SELECT {columna} FROM alimento LIMIT 3')
        muestras = cursor.fetchall()
        
        print(f"   📊 {columna}:")
        print(f"      - Registros no vacíos: {no_vacios}/{total_registros}")
        print(f"      - Ejemplos: {[m[0] for m in muestras]}")
    
    # 4. Ejecutar la consulta exacta del endpoint
    print("\n4️⃣ EJECUTANDO CONSULTA EXACTA DEL ENDPOINT:")
    query_endpoint = """
    SELECT ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as '#', 
           fecha, frecuencia_toma, estanque as estanque_celda, 
           tipo_alimento as referencia_alimento, cantidad_kg as cantidad_alimento, 
           mortalidad, causa_mortalidad, acciones_correctivas 
    FROM alimento WHERE 1=1 ORDER BY fecha DESC
    """
    
    cursor.execute(query_endpoint)
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    
    print(f"   📋 Columnas resultado: {columns}")
    print(f"   📈 Registros obtenidos: {len(rows)}")
    
    if rows:
        print("\n   📊 PRIMER REGISTRO COMPLETO:")
        for i, (col, valor) in enumerate(zip(columns, rows[0])):
            print(f"      {i+1}. {col}: '{valor}'")
    
    # 5. Verificar si hay valores NULL o vacíos
    print("\n5️⃣ VERIFICANDO VALORES NULL O VACÍOS:")
    for row_num, row in enumerate(rows[:3], 1):
        print(f"\n   Registro {row_num}:")
        for col_num, (col, valor) in enumerate(zip(columns, row)):
            estado = "✅" if valor not in [None, '', 'NULL'] else "⚠️"
            print(f"      {estado} {col}: '{valor}'")
    
    # 6. Comparar con los nombres esperados en la interfaz
    print("\n6️⃣ MAPEO COLUMNAS SQL → INTERFAZ:")
    nombres_interfaz = ['#', 'Fecha', 'Frecuencia Toma', 'Estanque/Celda', 
                       'Referencia Alimento', 'Cantidad Alimento', 'Mortalidad', 
                       'Causa Mortalidad', 'Acciones Correctivas']
    
    for i, (col_sql, nombre_interfaz) in enumerate(zip(columns, nombres_interfaz)):
        print(f"   {i+1}. {col_sql} → {nombre_interfaz}")
    
    conn.close()

if __name__ == "__main__":
    analizar_datos_alimento_completo()
