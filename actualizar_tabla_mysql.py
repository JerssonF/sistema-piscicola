import mysql.connector
from mysql.connector import Error

def actualizar_tabla():
    try:
        # Conexión MySQL
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='piscicola',
            charset='utf8mb4'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("🔧 ACTUALIZANDO TABLA ingreso_alimentos...")
            print("=" * 50)
            
            # Agregar columnas faltantes
            columnas_agregar = [
                "ADD COLUMN estanque VARCHAR(50)",
                "ADD COLUMN referencia_alimento VARCHAR(100)",
                "ADD COLUMN cantidad_alimento DECIMAL(10,2) DEFAULT 0",
                "ADD COLUMN frecuencia_toma VARCHAR(100)",
                "ADD COLUMN mortalidad INT DEFAULT 0",
                "ADD COLUMN causa_mortalidad TEXT",
                "ADD COLUMN acciones_correctivas TEXT",
                "ADD COLUMN fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
            ]
            
            for i, columna in enumerate(columnas_agregar):
                try:
                    query = f"ALTER TABLE ingreso_alimentos {columna}"
                    cursor.execute(query)
                    print(f"✅ Columna {i+1}/8 agregada: {columna.split()[2]}")
                except Error as e:
                    if "Duplicate column name" in str(e):
                        print(f"⚠️  Columna ya existe: {columna.split()[2]}")
                    else:
                        print(f"❌ Error agregando columna: {e}")
            
            connection.commit()
            print("\n🎉 ¡Tabla actualizada correctamente!")
            
            # Verificar estructura actualizada
            print("\n📊 NUEVA ESTRUCTURA:")
            print("=" * 30)
            cursor.execute("DESCRIBE ingreso_alimentos")
            columns = cursor.fetchall()
            
            for col in columns:
                print(f"- {col[0]} ({col[1]})")
                
    except Error as e:
        print(f"❌ Error de conexión MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    actualizar_tabla()