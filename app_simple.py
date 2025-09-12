from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'piscicola_secret_key_2025'

def get_db_connection():
    """Obtener conexión a la base de datos"""
    try:
        return sqlite3.connect('piscicola.db')
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

# ==================== RUTAS PRINCIPALES ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        
        # Validación simple
        if user == 'admin' and pwd == 'admin123':
            session['logged_in'] = True
            session['username'] = user
            return redirect(url_for('dashboard'))
        else:
            flash("Usuario o contraseña incorrectos.", "error")
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Obtener algunos datos para el dashboard
    alimentos = []
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alimento ORDER BY fecha DESC LIMIT 10")
            rows = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            alimentos = [dict(zip(columns, row)) for row in rows]
            
        except Exception as e:
            print(f"Error en dashboard: {e}")
        finally:
            conn.close()
    
    return render_template('dashboard.html', alimentos=alimentos)

@app.route('/test_api')
def test_api():
    """Ruta de prueba para verificar que la API funciona"""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return f'''
    <h1>Prueba de API</h1>
    <p><a href="/filtrar_informes?formulario=alimento">Probar filtro de alimentos</a></p>
    <p><a href="/filtrar_informes?formulario=muestreo">Probar filtro de muestreo</a></p>
    <p><a href="/filtrar_informes?formulario=parametros">Probar filtro de parámetros</a></p>
    <p><a href="/filtrar_informes?formulario=siembra">Probar filtro de siembra</a></p>
    <p><a href="/dashboard">Volver al dashboard</a></p>
    '''

@app.route('/formulario_informes')
def formulario_informes():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('formulario_informes_final.html')

# ==================== RUTA PARA FILTRAR INFORMES ====================

@app.route('/filtrar_informes')
def filtrar_informes():
    print("🔍 === RUTA FILTRAR_INFORMES EJECUTADA ===")
    print(f"📥 Parámetros recibidos: {dict(request.args)}")
    
    try:
        formulario = request.args.get('formulario')
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        estanque = request.args.get('estanque')
        
        print(f"✅ Formulario: {formulario}")
        print(f"✅ Fecha inicio: {fecha_inicio}")
        print(f"✅ Fecha fin: {fecha_fin}")
        print(f"✅ Estanque: {estanque}")
        
        if not formulario:
            return jsonify({'success': False, 'message': 'Formulario no especificado'})
        
        # Construir la consulta según el formulario
        queries = {
            'alimento': "SELECT fecha, estanque, tipo_alimento, cantidad_kg as cantidad, observaciones FROM alimento WHERE 1=1",
            'muestreo': "SELECT fecha, estanque, peso_promedio, cantidad_peces, (peso_promedio * cantidad_peces / 1000) as biomasa, observaciones FROM muestreo WHERE 1=1",
            'parametros': "SELECT fecha, estanque, temperatura, ph, oxigeno, observaciones FROM parametros WHERE 1=1",
            'siembra': "SELECT fecha, estanque, especie, cantidad as cantidad_alevinos, peso_promedio, observaciones FROM siembra WHERE 1=1"
        }
        
        if formulario not in queries:
            return jsonify({'success': False, 'message': f'Formulario no válido: {formulario}'})
        
        query = queries[formulario]
        params = []
        
        # Agregar filtros
        if fecha_inicio:
            query += " AND fecha >= ?"
            params.append(fecha_inicio)
            
        if fecha_fin:
            query += " AND fecha <= ?"
            params.append(fecha_fin)
            
        if estanque:
            query += " AND estanque = ?"
            params.append(estanque)
        
        query += " ORDER BY fecha DESC"
        
        print(f"🔍 Query final: {query}")
        print(f"📋 Parámetros: {params}")
        
        # Ejecutar consulta
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Error de conexión a la base de datos'})
        
        try:
            cursor = conn.cursor()
            print(f"🔍 Ejecutando query: {query}")
            print(f"📋 Con parámetros: {params}")
            cursor.execute(query, params)
            
            # Obtener resultados
            columns = [description[0] for description in cursor.description]
            print(f"🏷️ Columnas devueltas por SQLite: {columns}")
            resultados = []
            
            for row in cursor.fetchall():
                resultado = dict(zip(columns, row))
                resultados.append(resultado)
                
            print(f"📊 Primer resultado: {resultados[0] if resultados else 'Sin datos'}")
            
            conn.close()
            
            print(f"✅ Consulta exitosa - Resultados encontrados: {len(resultados)}")
            
            return jsonify({
                'success': True,
                'datos': resultados,
                'total': len(resultados)
            })
            
        except sqlite3.Error as e:
            conn.close()
            print(f"❌ Error de base de datos: {str(e)}")
            return jsonify({'success': False, 'message': f'Error de consulta: {str(e)}'})
            
    except Exception as e:
        print(f"❌ Error interno: {str(e)}")
        return jsonify({'success': False, 'message': f'Error interno: {str(e)}'})

# ==================== OTRAS RUTAS ====================

@app.route('/formulario_alimentos')
def formulario_alimentos():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('formulario_alimentos.html')

@app.route('/formulario_muestreo')
def formulario_muestreo():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('formulario_muestreo.html')

@app.route('/formulario_parametros')
def formulario_parametros():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('formulario_parametros.html')

@app.route('/formulario_siembra')
def formulario_siembra():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('formulario_siembra.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ==================== INICIALIZACIÓN ====================

def init_db():
    """Inicializar base de datos"""
    try:
        from database_config import init_db as db_init
        return db_init()
    except Exception as e:
        print(f"Error inicializando BD: {e}")
        return False

if __name__ == '__main__':
    print("🚀 === INICIANDO APLICACIÓN PISCÍCOLA ===")
    
    # Inicializar base de datos
    if init_db():
        print("✅ Base de datos inicializada correctamente")
    else:
        print("⚠️ Advertencia: No se pudo inicializar la base de datos")
    
    # Mostrar rutas disponibles
    print("\n📋 Rutas disponibles:")
    print("  / - Página principal")
    print("  /login - Iniciar sesión")
    print("  /dashboard - Panel principal")
    print("  /formulario_informes - Formulario de informes")
    print("  /filtrar_informes - API para filtrar datos")
    print("  /logout - Cerrar sesión")
    
    print("\n🌐 Servidor iniciando en: http://127.0.0.1:5000")
    print("👤 Usuario: admin | Contraseña: admin123")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
