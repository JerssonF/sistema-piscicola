#!/usr/bin/env python3
"""
Diagnóstico completo de problemas con los formularios de alimentos
"""
import sqlite3
from datetime import datetime

def verificar_estado_aplicacion():
    """Verificar el estado actual de la aplicación"""
    print("🔍 DIAGNÓSTICO COMPLETO DE FORMULARIOS DE ALIMENTOS")
    print("=" * 60)
    
    print("\n1. 📊 VERIFICANDO BASE DE DATOS:")
    try:
        conn = sqlite3.connect('piscicola.db')
        cursor = conn.cursor()
        
        # Verificar tabla alimento
        cursor.execute("SELECT COUNT(*) FROM alimento")
        total_alimentos = cursor.fetchone()[0]
        print(f"   ✅ Total registros en tabla 'alimento': {total_alimentos}")
        
        # Verificar últimos registros
        cursor.execute("SELECT id, fecha, hora, estanque, tipo_alimento, cantidad_kg, created_at FROM alimento ORDER BY created_at DESC LIMIT 3")
        ultimos = cursor.fetchall()
        
        print(f"\n   📝 Últimos 3 registros:")
        for reg in ultimos:
            print(f"      ID:{reg[0]} | {reg[1]} {reg[2]} | {reg[3]} | {reg[4]} | {reg[5]}kg | {reg[6]}")
        
        # Verificar registros de hoy
        cursor.execute("SELECT COUNT(*) FROM alimento WHERE DATE(created_at) = DATE('now')")
        hoy = cursor.fetchone()[0]
        print(f"\n   📅 Registros de hoy: {hoy}")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error en base de datos: {e}")

def verificar_rutas_flask():
    """Verificar que las rutas Flask estén configuradas correctamente"""
    print(f"\n2. 🔗 VERIFICANDO RUTAS FLASK:")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        rutas_esperadas = [
            '@app.route(\'/formulario_alimentos\'',
            '@app.route(\'/formulario_ingreso_alimento\'',
            'def formulario_alimentos():',
            'def formulario_ingreso_alimento():'
        ]
        
        for ruta in rutas_esperadas:
            if ruta in contenido:
                print(f"   ✅ {ruta}")
            else:
                print(f"   ❌ {ruta} - NO ENCONTRADA")
                
    except Exception as e:
        print(f"   ❌ Error leyendo app.py: {e}")

def verificar_templates():
    """Verificar que los templates existan"""
    print(f"\n3. 📄 VERIFICANDO TEMPLATES:")
    
    import os
    templates = [
        'templates/formulario_alimentos.html',
        'templates/formulario_ingreso_alimento.html',
        'templates/dashboard.html'
    ]
    
    for template in templates:
        if os.path.exists(template):
            print(f"   ✅ {template} - EXISTE")
        else:
            print(f"   ❌ {template} - NO EXISTE")

def simular_envio_datos():
    """Simular envío de datos para probar el guardado"""
    print(f"\n4. 🧪 SIMULANDO ENVÍO DE DATOS:")
    
    datos_test = {
        'fecha': '2025-09-05',
        'hora': '16:30',
        'estanque_celda': '1',
        'referencia_alimento': 'Pellet Test',
        'cantidad_alimento': '10.5',
        'frecuencia_toma': 'Test cada hora',
        'mortalidad': '0',
        'causa_mortalidad': 'Ninguna',
        'acciones_correctivas': 'Monitoreo continuo'
    }
    
    print("   📝 Datos de prueba:")
    for campo, valor in datos_test.items():
        print(f"      {campo}: {valor}")
    
    try:
        # Simular procesamiento como en app.py
        fecha = datos_test['fecha']
        hora = datos_test.get('hora', datetime.now().strftime('%H:%M'))
        estanque = datos_test['estanque_celda']
        tipo_alimento = datos_test['referencia_alimento']
        cantidad = float(datos_test['cantidad_alimento'])
        
        frecuencia_toma = datos_test.get('frecuencia_toma', '')
        mortalidad = int(datos_test.get('mortalidad', 0))
        causa_mortalidad = datos_test.get('causa_mortalidad', '')
        acciones_correctivas = datos_test.get('acciones_correctivas', '')
        
        observaciones = f"Frecuencia: {frecuencia_toma}; Mortalidad: {mortalidad}; Causa: {causa_mortalidad}; Acciones: {acciones_correctivas}"
        
        print(f"\n   ✅ Procesamiento de datos exitoso")
        print(f"      Observaciones: {observaciones[:60]}...")
        
        # Intentar guardar
        conn = sqlite3.connect('piscicola.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alimento (fecha, hora, estanque, tipo_alimento, cantidad_kg, observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (fecha, hora, estanque, tipo_alimento, cantidad, observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas))
        
        conn.commit()
        nuevo_id = cursor.lastrowid
        print(f"   ✅ Guardado exitoso - ID generado: {nuevo_id}")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error en simulación: {e}")

def verificar_aplicacion_web():
    """Verificar si la aplicación web está funcionando"""
    print(f"\n5. 🌐 VERIFICANDO APLICACIÓN WEB:")
    
    try:
        import requests
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print("   ✅ Aplicación web funcionando")
            
            # Probar rutas específicas
            rutas_test = [
                '/formulario_alimentos',
                '/formulario_ingreso_alimento'
            ]
            
            session = requests.Session()
            # Login
            login_data = {'username': 'admin', 'password': 'admin123'}
            login_response = session.post('http://localhost:5000/login', data=login_data)
            
            if login_response.status_code == 200:
                print("   ✅ Login exitoso")
                
                for ruta in rutas_test:
                    try:
                        resp = session.get(f'http://localhost:5000{ruta}')
                        if resp.status_code == 200:
                            print(f"   ✅ {ruta} - FUNCIONA")
                        else:
                            print(f"   ❌ {ruta} - ERROR {resp.status_code}")
                    except:
                        print(f"   ❌ {ruta} - NO RESPONDE")
            else:
                print("   ❌ Error en login")
        else:
            print(f"   ❌ Aplicación responde con error: {response.status_code}")
            
    except ImportError:
        print("   ⚠️  requests no instalado - no se puede probar web")
    except Exception as e:
        print(f"   ❌ Error verificando web: {e}")

def mostrar_recomendaciones():
    """Mostrar recomendaciones basadas en el diagnóstico"""
    print(f"\n6. 💡 RECOMENDACIONES:")
    print("   🔧 Para corregir problemas:")
    print("      1. Asegúrate de que la aplicación Flask esté ejecutándose")
    print("      2. Verifica que hayas hecho login antes de usar formularios")
    print("      3. Llena TODOS los campos requeridos del formulario")
    print("      4. Revisa la consola del navegador por errores JavaScript")
    print("      5. Verifica que no haya errores en el terminal de Flask")
    
    print(f"\n   📱 Para probar los formularios:")
    print("      • Formulario Alimentos: http://localhost:5000/formulario_alimentos")
    print("      • Ingreso Alimento: http://localhost:5000/formulario_ingreso_alimento")
    print("      • Ver datos guardados: http://localhost:5000/formulario_informes")

def main():
    """Función principal"""
    verificar_estado_aplicacion()
    verificar_rutas_flask()
    verificar_templates()
    simular_envio_datos()
    verificar_aplicacion_web()
    mostrar_recomendaciones()
    
    print(f"\n{'='*60}")
    print("🎯 CONCLUSIÓN DEL DIAGNÓSTICO")
    print("=" * 60)
    print("Si todos los tests anteriores son ✅, entonces:")
    print("• Los formularios DEBERÍAN funcionar correctamente")
    print("• El problema puede estar en el frontend o en el uso")
    print("• Verifica la consola del navegador por errores")

if __name__ == "__main__":
    main()
