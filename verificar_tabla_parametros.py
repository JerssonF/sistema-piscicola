import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('piscicola.db')
cursor = conn.cursor()

# Verificar estructura de la tabla parametros
print("=== ESTRUCTURA DE LA TABLA PARAMETROS ===")
cursor.execute('PRAGMA table_info(parametros)')
columns = cursor.fetchall()
for col in columns:
    print(f"Columna: {col[1]} | Tipo: {col[2]} | NotNull: {col[3]}")

print("\n=== DATOS DE MUESTRA ===")
cursor.execute('SELECT * FROM parametros LIMIT 3')
rows = cursor.fetchall()
column_names = [description[0] for description in cursor.description]
print("Columnas disponibles:", column_names)

for i, row in enumerate(rows):
    print(f"Fila {i+1}: {dict(zip(column_names, row))}")

conn.close()
