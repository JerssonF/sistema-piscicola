from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from config import Config
import os
import sqlite3

app = Flask(__name__)
app.config.from_object(Config)

def get_db_connection():
    """Conexión SQLite optimizada para producción"""
    try:
        if os.environ.get('RENDER'):
            # En Render, usar base de datos temporal
            db_path = '/tmp/piscicola.db'
        else:
            # Localmente
            db_path = os.path.join(os.path.dirname(__file__), 'piscicola.db')
        
        return sqlite3.connect(db_path)
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
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (user, pwd))
                usuario = cursor.fetchone()
                conn.close()
                
                if usuario:
                    session['logged_in'] = True
                    session['username'] = user
                    return redirect(url_for('dashboard'))
                else:
                    flash("Usuario o contraseña incorrectos.", "error")
            except Exception:
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
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alimento ORDER BY fecha DESC LIMIT 10")
            rows = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            alimentos = [dict(zip(columns, row)) for row in rows]
            
        except Exception:
            pass
        finally:
            conn.close()
    
    return render_template('dashboard.html', alimentos=alimentos)

@app.route('/formulario_alimentos', methods=['GET', 'POST'])
def formulario_alimentos():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        try:
            from datetime import datetime
            
            # Campos básicos
            fecha = request.form['fecha']
            hora = request.form.get('hora', datetime.now().strftime('%H:%M'))  # Si no hay hora, usar actual
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
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (fecha, hora, estanque, tipo_alimento, cantidad, observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas))
                
                conn.commit()
                flash("Alimento guardado correctamente.", "success")
                
            except Exception as e:
                flash(f"Error al guardar en la base de datos: {e}", "error")
            finally:
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
            tipo_alimento = request.form['ingreso_comida']
            cantidad = float(request.form['cantidad'])
            transporte = request.form.get('transporte', '')
            observaciones = request.form.get('observaciones', '')
            
            # Combinar observaciones con transporte si existe
            if transporte:
                observaciones = f"Transporte: {transporte}; {observaciones}"
            
        except (ValueError, KeyError) as e:
            flash(f"Verifica todos los campos del formulario: {e}", "error")
            return render_template('formulario_ingreso_alimento.html')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO alimento (fecha, hora, estanque, tipo_alimento, cantidad_kg, observaciones)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (fecha, hora, 'INGRESO', tipo_alimento, cantidad, observaciones))
                
                conn.commit()
                flash("Ingreso guardado correctamente.", "success")
                
            except Exception as e:
                flash(f"Error al guardar ingreso: {e}", "error")
            finally:
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
            
        except (ValueError, KeyError):
            flash("Verifica todos los campos del formulario.", "error")
            return render_template('formulario_muestreo.html')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO muestreo (fecha, hora, estanque, peso_promedio, talla_promedio, cantidad_peces, observaciones)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (fecha, hora, estanque, peso_promedio, talla_promedio, cantidad_peces, observaciones))
                
                conn.commit()
                flash("Muestreo registrado correctamente.", "success")
                
            except Exception:
                flash("Error al guardar muestreo.", "error")
            finally:
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
            
        except (ValueError, KeyError):
            flash("Verifica todos los campos del formulario.", "error")
            return render_template('formulario_parametros.html')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO parametros (fecha, hora, estanque, temperatura, ph, oxigeno, amonio, nitrito, nitrato, observaciones)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (fecha, hora, estanque, temperatura, ph, oxigeno, amonio, nitrito, nitrato, observaciones))
                
                conn.commit()
                flash("Parámetros registrados correctamente.", "success")
                
            except Exception:
                flash("Error al guardar parámetros.", "error")
            finally:
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
            
        except (ValueError, KeyError):
            flash("Verifica todos los campos del formulario.", "error")
            return render_template('formulario_siembra.html')
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO siembra (fecha, hora, estanque, especie, cantidad, peso_promedio, proveedor, observaciones)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (fecha, hora, estanque, especie, cantidad, peso_promedio, proveedor, observaciones))
                
                conn.commit()
                flash("Datos de siembra registrados correctamente.", "success")
                
            except Exception:
                flash("Error al guardar los datos de siembra.", "error")
            finally:
                conn.close()
        else:
            flash("Error de conexión a la base de datos.", "error")
            
        return redirect(url_for('formulario_siembra'))

    return render_template('formulario_siembra.html')

@app.route('/formulario_informes')
def formulario_informes():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('formulario_informes_nuevo.html')

# ==================== API PARA FILTRAR INFORMES ====================

@app.route('/filtrar_informes')
def filtrar_informes():
    try:
        # Agregar logging para debugging
        print(f"[DEBUG] Recibida petición: {request.args}")
        
        formulario = request.args.get('formulario')
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        estanque = request.args.get('estanque')
        
        if not formulario:
            return jsonify({'success': False, 'message': 'Formulario no especificado'})
        
        # Construir la consulta según el formulario con TODAS las columnas disponibles (sin ID interno)
        queries = {
            'alimento': {
                'query': "SELECT ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as 'Id', fecha, hora, estanque as estanque_celda, tipo_alimento as referencia_alimento, cantidad_kg as cantidad_alimento, observaciones, created_at, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas FROM alimento WHERE 1=1",
                'columns': ['Id', 'Fecha', 'Hora', 'Estanque/Celda', 'Referencia Alimento', 'Cantidad Alimento', 'Observaciones', 'Fecha Creación', 'Frecuencia Toma', 'Mortalidad', 'Causa Mortalidad', 'Acciones Correctivas']
            },
            'ingreso_alimentos': {
                'query': "SELECT ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as 'Id', fecha, hora, estanque as estanque_celda, tipo_alimento as referencia_alimento, cantidad_kg as cantidad_alimento, observaciones, created_at, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas FROM alimento WHERE 1=1",
                'columns': ['Id', 'Fecha', 'Hora', 'Estanque/Celda', 'Referencia Alimento', 'Cantidad Alimento', 'Observaciones', 'Fecha Creación', 'Frecuencia Toma', 'Mortalidad', 'Causa Mortalidad', 'Acciones Correctivas']
            },
            'muestreo': {
                'query': "SELECT ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as 'Id', fecha, hora, estanque as estanque_celda, peso_promedio, talla_promedio, cantidad_peces, observaciones, created_at, frecuencia_toma, especie, biomasa, peces FROM muestreo WHERE 1=1",
                'columns': ['Id', 'Fecha', 'Hora', 'Estanque/Celda', 'Peso Promedio', 'Talla Promedio', 'Cantidad Peces', 'Observaciones', 'Fecha Creación', 'Frecuencia Toma', 'Especie', 'Biomasa', 'Peces']
            },
            'parametros': {
                'query': "SELECT ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as 'Id', fecha, hora, estanque as estanque_celda, temperatura, ph, oxigeno, amonio, nitrito, nitrato, observaciones, created_at, frecuencia_toma, oxigeno_disuelto, nitritos FROM parametros WHERE 1=1",
                'columns': ['Id', 'Fecha', 'Hora', 'Estanque/Celda', 'Temperatura', 'pH', 'Oxígeno', 'Amonio', 'Nitrito', 'Nitrato', 'Observaciones', 'Fecha Creación', 'Frecuencia Toma', 'Oxígeno Disuelto', 'Nitritos']
            },
            'siembra': {
                'query': "SELECT ROW_NUMBER() OVER (ORDER BY fecha DESC, hora DESC) as 'Id', fecha, hora, estanque as estanque_celda, especie, cantidad, peso_promedio, proveedor, observaciones, created_at, destino, ovas_alevinos, hembras_machos FROM siembra WHERE 1=1",
                'columns': ['Id', 'Fecha', 'Hora', 'Estanque/Celda', 'Especie', 'Cantidad', 'Peso Promedio', 'Proveedor', 'Observaciones', 'Fecha Creación', 'Destino', 'Ovas/Alevinos', 'Hembras/Machos']
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
            query += " AND fecha >= ?"
            params.append(fecha_inicio)
            
        if fecha_fin:
            query += " AND fecha <= ?"
            params.append(fecha_fin)
            
        if estanque:
            # Usar el nombre de columna correcto según el formulario
            if formulario == 'alimento':
                query += " AND estanque = ?"
            elif formulario == 'muestreo':
                query += " AND estanque = ?"
            elif formulario == 'parametros':
                query += " AND estanque = ?"
            elif formulario == 'siembra':
                query += " AND estanque = ?"
            params.append(estanque)
        
        query += " ORDER BY fecha DESC"
        
        print(f"[DEBUG] Query: {query}")
        print(f"[DEBUG] Params: {params}")
        
        # Ejecutar consulta
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Error de conexión a la base de datos'})
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            # Obtener nombres de columnas en el orden exacto de la consulta SELECT
            columns = [description[0] for description in cursor.description]
            raw_results = cursor.fetchall()
            
            # Crear resultados como lista de listas para preservar el orden exacto
            resultados = []
            for row in raw_results:
                # Crear diccionario usando el orden exacto de las columnas SELECT
                resultado = {}
                for i, col_name in enumerate(columns):
                    resultado[col_name] = row[i]
                resultados.append(resultado)
            
            conn.close()
            
            print(f"[DEBUG] Consulta ejecutada: {query}")
            print(f"[DEBUG] Orden de columnas SQL: {columns}")
            print(f"[DEBUG] Resultados encontrados: {len(resultados)}")
            if resultados:
                print(f"[DEBUG] Primer resultado: {resultados[0]}")
            
            return jsonify({
                'success': True,
                'datos': resultados,
                'total': len(resultados),
                'columnas': column_names,
                'columnas_sql': columns,  # Este es el orden correcto que debe usar el frontend
                'formulario': formulario
            })
            
        except sqlite3.Error as e:
            conn.close()
            print(f"[ERROR] Error de consulta: {e}")
            return jsonify({'success': False, 'message': f'Error de consulta: {str(e)}'})
            
    except Exception as e:
        print(f"[ERROR] Error interno: {e}")
        return jsonify({'success': False, 'message': f'Error interno: {str(e)}'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ==================== INICIALIZACIÓN ====================

def init_db():
    """Inicializar base de datos con datos de prueba para Render"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        
        # Crear tablas si no existen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alimento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque TEXT NOT NULL,
                tipo_alimento TEXT NOT NULL,
                cantidad_kg REAL NOT NULL,
                observaciones TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS muestreo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque TEXT NOT NULL,
                peso_promedio REAL NOT NULL,
                talla_promedio REAL NOT NULL,
                cantidad_peces INTEGER NOT NULL,
                observaciones TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parametros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque TEXT NOT NULL,
                temperatura REAL NOT NULL,
                ph REAL NOT NULL,
                oxigeno REAL NOT NULL,
                amonio REAL,
                nitrito REAL,
                nitrato REAL,
                observaciones TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS siembra (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estanque TEXT NOT NULL,
                especie TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                peso_promedio REAL NOT NULL,
                proveedor TEXT,
                observaciones TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar usuario por defecto
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE username = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                'INSERT INTO usuarios (username, password) VALUES (?, ?)',
                ('admin', 'admin123')
            )
        
        # Insertar datos de prueba solo si las tablas están vacías
        cursor.execute('SELECT COUNT(*) FROM alimento')
        if cursor.fetchone()[0] == 0:
            # Datos de prueba para Render
            alimentos_prueba = [
                ('2025-09-01', '08:00', 'Estanque 1', 'Pellet Premium 4mm', 15.50, 'Alimentación matutina'),
                ('2025-09-01', '08:30', 'Estanque 2', 'Concentrado especial', 20.00, 'Alimentación vespertina'),
                ('2025-08-31', '09:00', 'Estanque 1', 'Pellet crecimiento', 18.75, 'Incremento por crecimiento'),
            ]
            
            cursor.executemany(
                "INSERT INTO alimento (fecha, hora, estanque, tipo_alimento, cantidad_kg, observaciones) VALUES (?, ?, ?, ?, ?, ?)",
                alimentos_prueba
            )
            
            # Datos de muestreo
            muestreo_prueba = [
                ('2025-09-01', '10:00', 'Estanque 1', 150.5, 12.3, 100, 'Crecimiento normal'),
                ('2025-08-31', '10:30', 'Estanque 2', 175.2, 13.1, 85, 'Buen desarrollo'),
            ]
            
            cursor.executemany(
                "INSERT INTO muestreo (fecha, hora, estanque, peso_promedio, talla_promedio, cantidad_peces, observaciones) VALUES (?, ?, ?, ?, ?, ?, ?)",
                muestreo_prueba
            )
            
            # Datos de parámetros
            parametros_prueba = [
                ('2025-09-01', '07:00', 'Estanque 1', 24.5, 7.2, 6.8, 0.1, 0.05, 0.2, 'Parámetros óptimos'),
                ('2025-09-01', '07:15', 'Estanque 2', 25.0, 7.0, 6.5, 0.15, 0.08, 0.25, 'Dentro del rango'),
            ]
            
            cursor.executemany(
                "INSERT INTO parametros (fecha, hora, estanque, temperatura, ph, oxigeno, amonio, nitrito, nitrato, observaciones) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                parametros_prueba
            )
            
            # Datos de siembra
            siembra_prueba = [
                ('2025-08-28', '08:00', 'Estanque 1', 'Tilapia', 1000, 0.5, 'Proveedor Local', 'Siembra inicial'),
                ('2025-08-28', '09:00', 'Estanque 2', 'Cachama', 800, 0.8, 'Acuícola del Norte', 'Segunda siembra'),
            ]
            
            cursor.executemany(
                "INSERT INTO siembra (fecha, hora, estanque, especie, cantidad, peso_promedio, proveedor, observaciones) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                siembra_prueba
            )
        
        conn.commit()
        conn.close()
        print("✅ Base de datos inicializada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando BD: {e}")
        return False

# Inicializar base de datos al inicio
try:
    init_db()
except Exception as e:
    print(f"❌ Error inicializando BD: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = not os.environ.get('RENDER')  # Debug solo en desarrollo
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
