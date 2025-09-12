import sqlite3

def verificar_estructura_alimento():
    print("============================================================")
    print("🔍 VERIFICACIÓN: ESTRUCTURA TABLA ALIMENTO")
    print("============================================================")
    
    try:
        conn = sqlite3.connect('piscicola.db')
        cursor = conn.cursor()
        
        # Ver estructura de la tabla
        cursor.execute("PRAGMA table_info(alimento)")
        columnas = cursor.fetchall()
        print("\n📊 COLUMNAS DE LA TABLA ALIMENTO:")
        for col in columnas:
            print(f"   {col[1]} ({col[2]})")
        
        # Ver todos los registros
        cursor.execute("SELECT * FROM alimento")
        registros = cursor.fetchall()
        print(f"\n📋 TOTAL REGISTROS: {len(registros)}")
        
        if registros:
            print("\n🔍 PRIMEROS 3 REGISTROS:")
            for i, registro in enumerate(registros[:3]):
                print(f"   Registro {i+1}: {registro}")
        
        # Ver tipos de estanque únicos
        cursor.execute("SELECT DISTINCT estanque FROM alimento")
        estanques = [row[0] for row in cursor.fetchall()]
        print(f"\n🏊 ESTANQUES ENCONTRADOS: {estanques}")
        
        conn.close()
        
        print("\n🎯 ANÁLISIS:")
        print("   Los estanques son números, no texto 'INGRESO'")
        print("   Necesitamos ajustar la consulta o los datos")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_estructura_alimento()
