#!/usr/bin/env python3
"""
Diagnóstico específico para problemas con el formulario de alimentos
"""
import mysql.connector
from mysql.connector import Error
from database_config_mysql import get_mysql_connection
import requests

def verificar_estado_mysql():
    """Verifica el estado actual de MySQL"""
    
    print("🔍 DIAGNÓSTICO: FORMULARIO DE ALIMENTOS")
    print("=" * 60)
    
    print("\n1. 📊 VERIFICANDO ESTADO ACTUAL DE MYSQL:")
    
    conn = get_mysql_connection()
    if not conn:
        print("❌ ERROR: No se puede conectar a MySQL")
        print("   - Verifica que XAMPP/WAMP esté ejecutándose")
        print("   - Verifica que MySQL esté activo en puerto 3306")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verificar base de datos
        cursor.execute("SELECT DATABASE()")
        db_actual = cursor.fetchone()[0]
        print(f"   ✅ Conectado a base de datos: {db_actual}")
        
        # Contar registros actuales
        cursor.execute("SELECT COUNT(*) FROM alimento")
        total_actual = cursor.fetchone()[0]
        print(f"   📊 Registros actuales en tabla alimento: {total_actual}")
        
        # Mostrar últimos registros con timestamp
        cursor.execute("SELECT id, fecha, hora, tipo_alimento, cantidad_kg, created_at FROM alimento ORDER BY id DESC LIMIT 3")
        registros = cursor.fetchall()
        
        if registros:
            print("   📋 Últimos registros:")
            for reg in registros:
                print(f"      ID:{reg[0]} | {reg[1]} {reg[2]} | {reg[3]} | {reg[4]}kg | {reg[5]}")
        else:
            print("   ⚠️  No hay registros en la tabla")
        
        cursor.close()
        conn.close()
        return True, total_actual
        
    except Error as e:
        print(f"❌ Error MySQL: {e}")
        if conn.is_connected():
            conn.close()
        return False, 0

def verificar_aplicacion_web():
    """Verifica que la aplicación web esté funcionando"""
    
    print("\n2. 🌐 VERIFICANDO APLICACIÓN WEB:")
    
    try:
        # Verificar que la aplicación responda
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print("   ✅ Aplicación web respondiendo correctamente")
        else:
            print(f"   ⚠️  Aplicación web responde con código: {response.status_code}")
        
        # Verificar ruta de login
        response = requests.get('http://localhost:5000/login', timeout=5)
        if response.status_code == 200:
            print("   ✅ Página de login accesible")
        else:
            print("   ❌ Problema con página de login")
        
        # Verificar ruta del formulario
        response = requests.get('http://localhost:5000/formulario_alimentos', timeout=5)
        if response.status_code in [200, 302]:  # 302 = redirect to login
            print("   ✅ Formulario de alimentos accesible")
        else:
            print("   ❌ Problema con formulario de alimentos")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ❌ ERROR: No se puede conectar a la aplicación web")
        print("      - Verifica que python app_mysql.py esté ejecutándose")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return False

def simular_envio_formulario():
    """Simula el envío del formulario para detectar problemas"""
    
    print("\n3. 🧪 SIMULANDO ENVÍO DE FORMULARIO:")
    
    # Datos de prueba que coinciden con el formulario HTML
    datos_formulario = {
        'fecha': '2025-09-05',
        'hora': '17:30',
        'frecuencia_toma': 'Cada 2 horas',
        'estanque_celda': '1',
        'referencia_alimento': 'Pellet Premium Diagnóstico',
        'cantidad_alimento': '15.5',
        'mortalidad': '0',
        'causa_mortalidad': 'Ninguna',
        'acciones_correctivas': 'Monitoreo regular'
    }
    
    print("   📝 Datos a enviar:")
    for campo, valor in datos_formulario.items():
        print(f"      {campo}: {valor}")
    
    try:
        # Crear sesión para mantener login
        session = requests.Session()
        
        # 1. Hacer login
        print("\n   🔐 Paso 1: Realizando login...")
        login_data = {'username': 'admin', 'password': 'admin123'}
        login_response = session.post('http://localhost:5000/login', data=login_data, timeout=10)
        
        if login_response.status_code == 200 and 'dashboard' in login_response.url:
            print("   ✅ Login exitoso")
        elif login_response.status_code == 302:
            print("   ✅ Login exitoso (redirección)")
        else:
            print(f"   ❌ Error en login: {login_response.status_code}")
            return False
        
        # 2. Enviar formulario
        print("   📤 Paso 2: Enviando formulario...")
        form_response = session.post('http://localhost:5000/formulario_alimentos', 
                                   data=datos_formulario, timeout=10)
        
        if form_response.status_code == 200:
            print("   ✅ Formulario enviado correctamente (200)")
        elif form_response.status_code == 302:
            print("   ✅ Formulario enviado correctamente (302 - redirect)")
        else:
            print(f"   ❌ Error enviando formulario: {form_response.status_code}")
            print(f"      Contenido: {form_response.text[:200]}...")
            return False
        
        # 3. Verificar si se guardó en BD
        print("   🔍 Paso 3: Verificando guardado en BD...")
        conn = get_mysql_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM alimento WHERE tipo_alimento LIKE '%Diagnóstico%'")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            if count > 0:
                print(f"   ✅ ¡DATOS GUARDADOS! Encontrados {count} registros de diagnóstico")
                return True
            else:
                print("   ❌ Los datos NO se guardaron en la base de datos")
                return False
        else:
            print("   ❌ No se pudo verificar la base de datos")
            return False
            
    except requests.exceptions.Timeout:
        print("   ❌ Timeout: La aplicación no responde")
        return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Error de conexión: Aplicación no disponible")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return False

def mostrar_solucion(problema_detectado):
    """Muestra la solución según el problema detectado"""
    
    print(f"\n{'='*60}")
    print("💡 SOLUCIÓN RECOMENDADA")
    print("=" * 60)
    
    if problema_detectado == "mysql_conexion":
        print("🔧 PROBLEMA: No se puede conectar a MySQL")
        print("   SOLUCIÓN:")
        print("   1. Abre XAMPP Control Panel")
        print("   2. Inicia el servicio MySQL")
        print("   3. Verifica que esté en puerto 3306")
        print("   4. Vuelve a intentar")
        
    elif problema_detectado == "aplicacion_web":
        print("🔧 PROBLEMA: Aplicación web no responde")
        print("   SOLUCIÓN:")
        print("   1. Ejecuta: python app_mysql.py")
        print("   2. Verifica que no haya errores en la consola")
        print("   3. Abre http://localhost:5000")
        
    elif problema_detectado == "formulario_guardado":
        print("🔧 PROBLEMA: El formulario no guarda en la base de datos")
        print("   POSIBLES CAUSAS:")
        print("   - Error en la estructura de la tabla")
        print("   - Campos del formulario HTML no coinciden con app_mysql.py")
        print("   - Error en la consulta SQL")
        print("   SOLUCIÓN:")
        print("   1. Revisa los logs de la aplicación")
        print("   2. Verifica la estructura de la tabla alimento")
        print("   3. Comprueba que los nombres de campos coincidan")
        
    else:
        print("✅ TODO FUNCIONA CORRECTAMENTE")
        print("   Si aún no ves los datos:")
        print("   1. Ve a phpMyAdmin: http://localhost/phpmyadmin")
        print("   2. Selecciona base de datos 'piscicola'")
        print("   3. Haz clic en tabla 'alimento'")
        print("   4. Deberías ver todos los registros")

def main():
    """Función principal de diagnóstico"""
    
    problema_detectado = None
    
    # Verificar MySQL
    mysql_ok, registros_iniciales = verificar_estado_mysql()
    if not mysql_ok:
        problema_detectado = "mysql_conexion"
    
    # Verificar aplicación web
    if mysql_ok:
        web_ok = verificar_aplicacion_web()
        if not web_ok:
            problema_detectado = "aplicacion_web"
    
    # Simular envío si todo está bien
    if mysql_ok and web_ok:
        guardado_ok = simular_envio_formulario()
        if not guardado_ok:
            problema_detectado = "formulario_guardado"
    
    # Mostrar solución
    mostrar_solucion(problema_detectado)
    
    print(f"\n{'='*60}")
    if problema_detectado:
        print("❌ SE DETECTARON PROBLEMAS")
    else:
        print("✅ DIAGNÓSTICO COMPLETADO - TODO FUNCIONA")
    print("=" * 60)

if __name__ == "__main__":
    main()
