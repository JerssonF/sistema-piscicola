#!/usr/bin/env python3
"""
Script para migrar datos de SQLite a MySQL
"""
import sqlite3
import mysql.connector
from mysql.connector import Error
from database_config_mysql import get_mysql_connection

def migrar_datos_sqlite_a_mysql():
    """Migra todos los datos de SQLite a MySQL"""
    
    print("🔄 MIGRACIÓN DE DATOS: SQLite → MySQL")
    print("=" * 50)
    
    # Conectar a SQLite
    try:
        sqlite_conn = sqlite3.connect('piscicola.db')
        sqlite_cursor = sqlite_conn.cursor()
        print("✅ Conexión SQLite establecida")
    except Exception as e:
        print(f"❌ Error conectando a SQLite: {e}")
        return False
    
    # Conectar a MySQL
    mysql_conn = get_mysql_connection()
    if not mysql_conn:
        print("❌ Error conectando a MySQL")
        return False
    
    print("✅ Conexión MySQL establecida")
    
    try:
        mysql_cursor = mysql_conn.cursor()
        
        # Migrar tabla usuarios
        print("\n📋 Migrando usuarios...")
        sqlite_cursor.execute("SELECT username, password, created_at FROM usuarios")
        usuarios = sqlite_cursor.fetchall()
        
        for usuario in usuarios:
            try:
                mysql_cursor.execute(
                    "INSERT IGNORE INTO usuarios (username, password, created_at) VALUES (%s, %s, %s)",
                    usuario
                )
            except Error as e:
                print(f"⚠️  Error insertando usuario {usuario[0]}: {e}")
        
        print(f"✅ {len(usuarios)} usuarios migrados")
        
        # Migrar tabla alimento
        print("\n🍽️  Migrando alimentos...")
        sqlite_cursor.execute("""
            SELECT fecha, hora, estanque, tipo_alimento, cantidad_kg, observaciones, 
                   created_at, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas
            FROM alimento
        """)
        alimentos = sqlite_cursor.fetchall()
        
        for alimento in alimentos:
            try:
                mysql_cursor.execute("""
                    INSERT INTO alimento (fecha, hora, estanque, tipo_alimento, cantidad_kg, observaciones, 
                                        created_at, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, alimento)
            except Error as e:
                print(f"⚠️  Error insertando alimento: {e}")
        
        print(f"✅ {len(alimentos)} alimentos migrados")
        
        # Migrar tabla muestreo
        print("\n🔬 Migrando muestreos...")
        try:
            sqlite_cursor.execute("""
                SELECT fecha, hora, estanque, peso_promedio, talla_promedio, cantidad_peces, 
                       observaciones, created_at
                FROM muestreo
            """)
            muestreos = sqlite_cursor.fetchall()
            
            for muestreo in muestreos:
                try:
                    mysql_cursor.execute("""
                        INSERT INTO muestreo (fecha, hora, estanque, peso_promedio, talla_promedio, 
                                            cantidad_peces, observaciones, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, muestreo)
                except Error as e:
                    print(f"⚠️  Error insertando muestreo: {e}")
            
            print(f"✅ {len(muestreos)} muestreos migrados")
        except sqlite3.OperationalError:
            print("⚠️  Tabla muestreo no existe en SQLite")
        
        # Migrar tabla parametros
        print("\n⚙️  Migrando parámetros...")
        try:
            sqlite_cursor.execute("""
                SELECT fecha, hora, estanque, temperatura, ph, oxigeno, amonio, nitrito, nitrato, 
                       observaciones, created_at
                FROM parametros
            """)
            parametros = sqlite_cursor.fetchall()
            
            for parametro in parametros:
                try:
                    mysql_cursor.execute("""
                        INSERT INTO parametros (fecha, hora, estanque, temperatura, ph, oxigeno, 
                                              amonio, nitrito, nitrato, observaciones, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, parametro)
                except Error as e:
                    print(f"⚠️  Error insertando parámetro: {e}")
            
            print(f"✅ {len(parametros)} parámetros migrados")
        except sqlite3.OperationalError:
            print("⚠️  Tabla parametros no existe en SQLite")
        
        # Migrar tabla siembra
        print("\n🌱 Migrando siembras...")
        try:
            sqlite_cursor.execute("""
                SELECT fecha, hora, estanque, especie, cantidad, peso_promedio, proveedor, 
                       observaciones, created_at
                FROM siembra
            """)
            siembras = sqlite_cursor.fetchall()
            
            for siembra in siembras:
                try:
                    mysql_cursor.execute("""
                        INSERT INTO siembra (fecha, hora, estanque, especie, cantidad, peso_promedio, 
                                           proveedor, observaciones, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, siembra)
                except Error as e:
                    print(f"⚠️  Error insertando siembra: {e}")
            
            print(f"✅ {len(siembras)} siembras migradas")
        except sqlite3.OperationalError:
            print("⚠️  Tabla siembra no existe en SQLite")
        
        # Confirmar cambios
        mysql_conn.commit()
        print("\n🎉 ¡Migración completada exitosamente!")
        
        # Mostrar resumen
        print("\n📊 RESUMEN DE MIGRACIÓN:")
        mysql_cursor.execute("SELECT COUNT(*) FROM usuarios")
        print(f"   👥 Usuarios: {mysql_cursor.fetchone()[0]}")
        
        mysql_cursor.execute("SELECT COUNT(*) FROM alimento")
        print(f"   🍽️  Alimentos: {mysql_cursor.fetchone()[0]}")
        
        try:
            mysql_cursor.execute("SELECT COUNT(*) FROM muestreo")
            print(f"   🔬 Muestreos: {mysql_cursor.fetchone()[0]}")
        except:
            print(f"   🔬 Muestreos: 0")
        
        try:
            mysql_cursor.execute("SELECT COUNT(*) FROM parametros")
            print(f"   ⚙️  Parámetros: {mysql_cursor.fetchone()[0]}")
        except:
            print(f"   ⚙️  Parámetros: 0")
        
        try:
            mysql_cursor.execute("SELECT COUNT(*) FROM siembra")
            print(f"   🌱 Siembras: {mysql_cursor.fetchone()[0]}")
        except:
            print(f"   🌱 Siembras: 0")
            
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False
        
    finally:
        sqlite_cursor.close()
        sqlite_conn.close()
        mysql_cursor.close()
        mysql_conn.close()

def verificar_datos_mysql():
    """Verifica que los datos estén en MySQL"""
    
    print(f"\n{'='*50}")
    print("🔍 VERIFICACIÓN DE DATOS EN MYSQL")
    print("=" * 50)
    
    conn = get_mysql_connection()
    if not conn:
        print("❌ No se pudo conectar a MySQL")
        return False
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Verificar alimentos recientes
        cursor.execute("SELECT * FROM alimento ORDER BY created_at DESC LIMIT 5")
        alimentos = cursor.fetchall()
        
        print(f"\n📋 Últimos 5 alimentos en MySQL:")
        for i, alimento in enumerate(alimentos, 1):
            print(f"   {i}. ID: {alimento['id']}, Fecha: {alimento['fecha']}, Tipo: {alimento['tipo_alimento']}")
            print(f"      Cantidad: {alimento['cantidad_kg']}kg, Estanque: {alimento['estanque']}")
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"❌ Error verificando datos: {e}")
        if conn.is_connected():
            conn.close()
        return False

def main():
    """Función principal"""
    if migrar_datos_sqlite_a_mysql():
        verificar_datos_mysql()
        
        print(f"\n{'='*50}")
        print("✅ MIGRACIÓN COMPLETADA")
        print("=" * 50)
        print("🎯 PRÓXIMOS PASOS:")
        print("   1. Usa 'python app_mysql.py' para ejecutar la aplicación con MySQL")
        print("   2. Ve a phpMyAdmin y verás la base de datos 'piscicola'")
        print("   3. Todos los formularios ahora guardarán en MySQL")
        print("   4. Los datos aparecerán en phpMyAdmin inmediatamente")
        
    else:
        print("\n❌ Error en la migración")

if __name__ == "__main__":
    main()
