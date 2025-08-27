import mysql.connector

# Conectar a la base de datos MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='piscicola'
)

cursor = connection.cursor(dictionary=True)

# Verificar qué tablas existen
print("=== TABLAS EXISTENTES ===")
cursor.execute("SHOW TABLES")
tablas = cursor.fetchall()
for tabla in tablas:
    table_name = list(tabla.values())[0]
    print(f"Tabla: {table_name}")

# Verificar datos de alimentos
print("\n=== ESTRUCTURA DE LA TABLA ALIMENTO ===")
cursor.execute("DESCRIBE alimento")
estructura = cursor.fetchall()
for campo in estructura:
    print(f"Campo: {campo['Field']}, Tipo: {campo['Type']}")

# Mostrar algunos datos de alimentos
print("\n=== DATOS DE ALIMENTO ===")
cursor.execute("SELECT * FROM alimento LIMIT 3")
datos = cursor.fetchall()
if datos:
    for dato in datos:
        print(dato)
else:
    print("No hay datos en la tabla alimento")

cursor.close()
connection.close()
