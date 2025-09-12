import mysql.connector
from mysql.connector import Error

def verificar_tabla():
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
            
            # Verificar estructura de la tabla ingreso_alimentos
            print("📊 ESTRUCTURA DE LA TABLA ingreso_alimentos:")
            print("=" * 50)
            
            cursor.execute("DESCRIBE ingreso_alimentos")
            columns = cursor.fetchall()
            
            for col in columns:
                print(f"- {col[0]} ({col[1]})")
                
            print("\n🔍 DATOS ACTUALES EN LA TABLA:")
            print("=" * 50)
            
            cursor.execute("SELECT * FROM ingreso_alimentos LIMIT 3")
            rows = cursor.fetchall()
            
            if rows:
                for i, row in enumerate(rows):
                    print(f"Registro {i+1}: {row}")
            else:
                print("No hay datos en la tabla")
                
            # Verificar si las columnas nuevas existen
            print("\n✅ VERIFICANDO COLUMNAS NUEVAS:")
            print("=" * 50)
            
            columnas_necesarias = [
                'estanque', 'referencia_alimento', 'cantidad_alimento', 
                'frecuencia_toma', 'mortalidad', 'causa_mortalidad', 
                'acciones_correctivas', 'fecha_creacion'
            ]
            
            columnas_existentes = [col[0] for col in columns]
            
            for col in columnas_necesarias:
                if col in columnas_existentes:
                    print(f"✅ {col} - EXISTE")
                else:
                    print(f"❌ {col} - NO EXISTE")
                    
    except Error as e:
        print(f"❌ Error de conexión MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    verificar_tabla()