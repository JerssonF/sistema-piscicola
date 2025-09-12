from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from config import Config
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config.from_object(Config)

# Configuración MySQL
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Cambia si tienes contraseña
    'database': 'piscicola',
    'charset': 'utf8mb4'
}

def get_db_connection():
    """Conexión MySQL para phpMyAdmin"""
    try:
        connection = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            database=MYSQL_CONFIG['database'],
            charset=MYSQL_CONFIG['charset']
        )
        return connection
    except Error as e:
        print(f"Error de conexión MySQL: {e}")
        return None

def serialize_mysql_data(data):
    """Convierte tipos MySQL no serializables a JSON"""
    if isinstance(data, list):
        return [serialize_mysql_data(item) for item in data]
    elif isinstance(data, dict):
        return {key: serialize_mysql_data(value) for key, value in data.items()}
    elif isinstance(data, timedelta):
        # Convertir timedelta a string en formato HH:MM:SS
        total_seconds = int(data.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    elif isinstance(data, datetime):
        # Convertir datetime a string
        return data.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return data

# ==================== RUTAS PRINCIPALES ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", (user, pwd))
                usuario = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if usuario:
                    session['logged_in'] = True
                    session['username'] = user
                    return redirect(url_for('dashboard'))
                else:
                    flash("Usuario o contraseña incorrectos.", "error")
            except Error:
                flash("Error de conexión", "error")
        else:
            flash("Error de conexión a la base de datos", "error")
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    alimentos = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM alimento ORDER BY fecha DESC LIMIT 10")
            alimentos = cursor.fetchall()
            cursor.close()
        except Error:
            pass
        finally:
            conn.close()
    
    return render_template('dashboard.html', alimentos=alimentos)

@app.route('/formulario_alimentos', methods=['GET', 'POST'])
def formulario_alimentos():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        print("📝 FORMULARIO POST RECIBIDO - Procesando datos...")
        try:
            # Campos básicos
            fecha = request.form['fecha']
            hora = request.form.get('hora', datetime.now().strftime('%H:%M'))
            estanque = request.form['estanque_celda']
            tipo_alimento = request.form['referencia_alimento']
            cantidad = float(request.form['cantidad_alimento'])
            
            # Campos adicionales del template
            frecuencia_toma = request.form.get('frecuencia_toma', '')
            mortalidad = int(request.form.get('mortalidad', 0))
            causa_mortalidad = request.form.get('causa_mortalidad', '')
            acciones_correctivas = request.form.get('acciones_correctivas', '')
            
            # Crear observaciones combinando los campos adicionales
            observaciones = f"Frecuencia: {frecuencia_toma}; Mortalidad: {mortalidad}; Causa: {causa_mortalidad}; Acciones: {acciones_correctivas}"
            
        except (ValueError, KeyError) as e:
            flash(f"Error en los datos del formulario: {e}", "error")
            return render_template('formulario_alimentos.html')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO alimento (fecha, hora, estanque, tipo_alimento, cantidad_kg, observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (fecha, hora, estanque, tipo_alimento, cantidad, observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas))
                
                conn.commit()
                flash("Alimento guardado correctamente.", "success")
                
            except Error as e:
                flash(f"Error al guardar en la base de datos: {e}", "error")
            finally:
                cursor.close()
                conn.close()
        else:
            flash("Error de conexión a la base de datos.", "error")
        
        return redirect(url_for('formulario_alimentos'))

    return render_template('formulario_alimentos.html')

@app.route('/formulario_ingreso_alimento', methods=['GET', 'POST'])
def formulario_ingreso_alimento():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        try:
            fecha = request.form['fecha']
            hora = request.form['hora']
            estanque = request.form.get('estanque', '')
            referencia_alimento = request.form.get('referencia_alimento', '')
            cantidad_alimento = float(request.form.get('cantidad_alimento', 0))
            frecuencia_toma = request.form.get('frecuencia_toma', '')
            mortalidad = int(request.form.get('mortalidad', 0))
            causa_mortalidad = request.form.get('causa_mortalidad', '')
            acciones_correctivas = request.form.get('acciones_correctivas', '')
            tipo_alimento = request.form['ingreso_comida']
            cantidad = float(request.form['cantidad'])
            observaciones = request.form.get('observaciones', '')
            transporte = request.form.get('transporte', '')
            
            # Combinar observaciones con transporte
            if transporte:
                observaciones = f"{observaciones}; Transporte: {transporte}"
            
        except (ValueError, KeyError) as e:
            flash(f"Error en los datos del formulario: {e}", "error")
            return render_template('formulario_ingreso_alimento.html')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO ingreso_alimentos (fecha, hora, estanque, referencia_alimento, cantidad_alimento, 
                                                 frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas,
                                                 ingreso_comida, cantidad, transporte, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (fecha, hora, estanque, referencia_alimento, cantidad_alimento, frecuencia_toma, 
                     mortalidad, causa_mortalidad, acciones_correctivas, tipo_alimento, cantidad, transporte, observaciones))
                
                conn.commit()
                flash("Ingreso de alimentos guardado correctamente.", "success")
                
            except Error as e:
                flash(f"Error al guardar ingreso: {e}", "error")
            finally:
                cursor.close()
                conn.close()
        else:
            flash("Error de conexión a la base de datos.", "error")
            
        return redirect(url_for('formulario_ingreso_alimento'))

    return render_template('formulario_ingreso_alimento.html')

@app.route('/formulario_muestreo', methods=['GET', 'POST'])
def formulario_muestreo():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        try:
            fecha = request.form['fecha']
            hora = request.form['hora']
            estanque = request.form['estanque_celda']
            peso_promedio = float(request.form['peso_promedio_g'])
            talla_promedio = float(request.form.get('talla_promedio', 0))
            cantidad_peces = int(request.form['peces'])
            observaciones = request.form.get('observaciones', '')
            
        except (ValueError, KeyError) as e:
            flash(f"Error en los datos del formulario: {e}", "error")
            return render_template('formulario_muestreo.html')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO muestreo (fecha, hora, estanque, peso_promedio, talla_promedio, cantidad_peces, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (fecha, hora, estanque, peso_promedio, talla_promedio, cantidad_peces, observaciones))
                
                conn.commit()
                flash("Muestreo registrado correctamente.", "success")
                
            except Error as e:
                flash(f"Error al guardar muestreo: {e}", "error")
            finally:
                cursor.close()
                conn.close()
        else:
            flash("Error de conexión a la base de datos.", "error")
            
        return redirect(url_for('formulario_muestreo'))

    return render_template('formulario_muestreo.html')

@app.route('/formulario_parametros', methods=['GET', 'POST'])
def formulario_parametros():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        try:
            fecha = request.form['fecha']
            hora = request.form['hora']
            estanque = request.form['estanque_celda']
            temperatura = float(request.form['temperatura'])
            ph = float(request.form['ph'])
            oxigeno = float(request.form['oxigeno'])
            amonio = float(request.form.get('amonio', 0))
            nitrito = float(request.form.get('nitrito', 0))
            nitrato = float(request.form.get('nitrato', 0))
            observaciones = request.form.get('observaciones', '')
            
        except (ValueError, KeyError) as e:
            flash(f"Error en los datos del formulario: {e}", "error")
            return render_template('formulario_parametros.html')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO parametros (fecha, hora, estanque, temperatura, ph, oxigeno, amonio, nitrito, nitrato, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (fecha, hora, estanque, temperatura, ph, oxigeno, amonio, nitrito, nitrato, observaciones))
                
                conn.commit()
                flash("Parámetros registrados correctamente.", "success")
                
            except Error as e:
                flash(f"Error al guardar parámetros: {e}", "error")
            finally:
                cursor.close()
                conn.close()
        else:
            flash("Error de conexión a la base de datos.", "error")
            
        return redirect(url_for('formulario_parametros'))

    return render_template('formulario_parametros.html')

@app.route('/formulario_siembra', methods=['GET', 'POST'])
def formulario_siembra():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            fecha = request.form['fecha']
            hora = request.form['hora_siembra']
            estanque = request.form['estanque_celda']
            especie = request.form['especie']
            cantidad = int(request.form['ovas_alevinos'])
            peso_promedio = float(request.form['peso_promedio'])
            proveedor = request.form.get('origen_semilla', '')
            observaciones = request.form.get('observaciones', '')
            
        except (ValueError, KeyError) as e:
            flash(f"Error en los datos del formulario: {e}", "error")
            return render_template('formulario_siembra.html')
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO siembra (fecha, hora, estanque, especie, cantidad, peso_promedio, proveedor, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', (fecha, hora, estanque, especie, cantidad, peso_promedio, proveedor, observaciones))
                
                conn.commit()
                flash("Datos de siembra registrados correctamente.", "success")
                
            except Error as e:
                flash(f"Error al guardar los datos de siembra: {e}", "error")
            finally:
                cursor.close()
                conn.close()
        else:
            flash("Error de conexión a la base de datos.", "error")
            
        return redirect(url_for('formulario_siembra'))

    return render_template('formulario_siembra.html')

@app.route('/formulario_informes', methods=['GET', 'POST'])
def formulario_informes():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Si es POST, procesar los filtros
    if request.method == 'POST':
        formulario = request.form.get('formulario')
        fecha_desde = request.form.get('fecha_desde')
        fecha_hasta = request.form.get('fecha_hasta')
        
        if formulario and fecha_desde and fecha_hasta:
            # Redirigir a la API de filtros con los parámetros
            return redirect(url_for('filtrar_informes', 
                                  formulario=formulario,
                                  fecha_inicio=fecha_desde, 
                                  fecha_fin=fecha_hasta))
    
    return render_template('formulario_informes_mejorado.html')

# ==================== API PARA FILTRAR INFORMES ====================

@app.route('/filtrar_informes')
def filtrar_informes():
    try:
        formulario = request.args.get('formulario')
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        estanque = request.args.get('estanque')
        
        if not formulario:
            return jsonify({'success': False, 'message': 'Formulario no especificado'})
        
        # Construir la consulta según el formulario
        queries = {
            'alimento': {
                'query': "SELECT ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as 'Id', fecha, hora, estanque, tipo_alimento, cantidad_kg, COALESCE(frecuencia_toma, '') as frecuencia_toma, COALESCE(mortalidad, 0) as mortalidad, COALESCE(causa_mortalidad, '') as causa_mortalidad, COALESCE(acciones_correctivas, '') as acciones_correctivas, COALESCE(observaciones, '') as observaciones FROM alimento WHERE 1=1",
                'columns': ['Id', 'Fecha', 'Hora', 'Estanque', 'Tipo Alimento', 'Cantidad (kg)', 'Frecuencia', 'Mortalidad', 'Causa Mortalidad', 'Acciones Correctivas', 'Observaciones']
            },
            'ingreso_alimentos': {
                'query': "SELECT ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as Id, fecha, hora, COALESCE(estanque, '') as estanque_celda, COALESCE(referencia_alimento, '') as referencia_alimento, COALESCE(cantidad_alimento, 0) as cantidad_alimento, COALESCE(observaciones, '') as observaciones, COALESCE(fecha_creacion, '') as fecha_creacion, COALESCE(frecuencia_toma, '') as frecuencia_toma, COALESCE(mortalidad, 0) as mortalidad, COALESCE(causa_mortalidad, '') as causa_mortalidad, COALESCE(acciones_correctivas, '') as acciones_correctivas FROM ingreso_alimentos WHERE 1=1",
                'columns': ['Id', 'Fecha', 'Hora', 'Estanque Celda', 'Referencia Alimento', 'Cantidad Alimento', 'Observaciones', 'Fecha Creación', 'Frecuencia Toma', 'Mortalidad', 'Causa Mortalidad', 'Acciones Correctivas']
            },
            'muestreo': {
                'query': "SELECT ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as 'Id', fecha, hora, estanque, COALESCE(especie, '') as especie, COALESCE(biomasa, 0) as biomasa, cantidad_peces, peso_promedio, talla_promedio, COALESCE(observaciones, '') as observaciones FROM muestreo WHERE 1=1",
                'columns': ['Id', 'Fecha', 'Hora', 'Estanque', 'Especie', 'Biomasa (kg)', 'Cantidad Peces', 'Peso Promedio (g)', 'Talla Promedio (cm)', 'Observaciones']
            },
            'parametros': {
                'query': "SELECT ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as 'Id', fecha, hora, estanque, temperatura, ph, oxigeno, COALESCE(amonio, 0) as amonio, COALESCE(nitrito, 0) as nitrito, COALESCE(nitrato, 0) as nitrato, COALESCE(observaciones, '') as observaciones FROM parametros WHERE 1=1",
                'columns': ['Id', 'Fecha', 'Hora', 'Estanque', 'Temperatura (°C)', 'pH', 'Oxígeno', 'Amonio', 'Nitrito', 'Nitrato', 'Observaciones']
            },
            'siembra': {
                'query': "SELECT ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as 'Id', fecha, hora, estanque, especie, cantidad, peso_promedio, COALESCE(proveedor, '') as proveedor, COALESCE(observaciones, '') as observaciones FROM siembra WHERE 1=1",
                'columns': ['Id', 'Fecha', 'Hora', 'Estanque', 'Especie', 'Cantidad', 'Peso Promedio (g)', 'Proveedor', 'Observaciones']
            }
        }
        
        if formulario not in queries:
            return jsonify({'success': False, 'message': f'Formulario no válido: {formulario}'})
        
        query_info = queries[formulario]
        query = query_info['query']
        column_names = query_info['columns']
        params = []
        
        # Agregar filtros
        if fecha_inicio:
            query += " AND fecha >= %s"
            params.append(fecha_inicio)
            
        if fecha_fin:
            query += " AND fecha <= %s"
            params.append(fecha_fin)
            
        if estanque:
            query += " AND estanque = %s"
            params.append(estanque)
        
        query += " ORDER BY fecha DESC"
        
        # Ejecutar consulta
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Error de conexión a la base de datos'})
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Serializar los datos para evitar errores de JSON
            datos_serializados = serialize_mysql_data(resultados)
            
            return jsonify({
                'success': True,
                'datos': datos_serializados,
                'total': len(resultados),
                'columnas': column_names,
                'formulario': formulario
            })
            
        except Error as e:
            if conn.is_connected():
                conn.close()
            return jsonify({'success': False, 'message': f'Error de consulta: {str(e)}'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error interno: {str(e)}'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ==================== INICIALIZACIÓN ====================

def init_db():
    """Inicializar base de datos MySQL"""
    from database_config_mysql import create_database, init_mysql_tables
    
    try:
        print("🔧 Inicializando base de datos MySQL...")
        
        # Crear base de datos
        if create_database():
            # Crear tablas
            if init_mysql_tables():
                print("✅ Base de datos MySQL inicializada correctamente")
                return True
            else:
                print("❌ Error creando tablas MySQL")
                return False
        else:
            print("❌ Error creando base de datos MySQL")
            return False
            
    except Exception as e:
        print(f"❌ Error inicializando BD MySQL: {e}")
        return False

# Inicializar base de datos al inicio
try:
    init_db()
except Exception as e:
    print(f"❌ Error inicializando BD: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = not os.environ.get('RENDER')
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
