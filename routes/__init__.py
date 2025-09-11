from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import datetime
import sys
import os

# Agregar el directorio raíz al path para importar database_config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_config import get_connection, init_db

bp = Blueprint('routes', __name__)

def get_db_connection():
    """Conexión SQLite para producción"""
    try:
        return get_connection()
    except Exception:
        return None

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
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
                    return redirect(url_for('routes.dashboard'))
                else:
                    flash("Usuario o contraseña incorrectos.", "error")
            except Exception:
                flash("Error de conexión", "error")
        else:
            flash("Error de conexión a la base de datos", "error")
    
    return render_template('login.html')

@bp.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))

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

@bp.route('/formulario_alimentos', methods=['GET', 'POST'])
def formulario_alimentos():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))
        
    if request.method == 'POST':
        try:
            fecha = request.form['fecha']
            hora = request.form['hora']
            estanque = request.form['estanque_celda']
            tipo_alimento = request.form['referencia_alimento']
            cantidad = float(request.form['cantidad_alimento'])
            observaciones = request.form.get('observaciones', '')
            
        except (ValueError, KeyError):
            flash("Verifica todos los campos del formulario.", "error")
            return render_template('formulario_alimentos.html')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO alimento (fecha, hora, estanque, tipo_alimento, cantidad_kg, observaciones)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (fecha, hora, estanque, tipo_alimento, cantidad, observaciones))
                
                conn.commit()
                flash("Alimento guardado correctamente.", "success")
                
            except Exception:
                flash("Error al guardar en la base de datos.", "error")
            finally:
                conn.close()
        else:
            flash("Error de conexión a la base de datos.", "error")
        
        return redirect(url_for('routes.formulario_alimentos'))

    return render_template('formulario_alimentos.html')

@bp.route('/formulario_ingreso_alimento', methods=['GET', 'POST'])
def formulario_ingreso_alimento():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))
        
    if request.method == 'POST':
        try:
            fecha = request.form['fecha']
            hora = request.form['hora']
            tipo_alimento = request.form['ingreso_comida']
            cantidad = float(request.form['cantidad'])
            observaciones = request.form.get('observaciones', '')
            
        except (ValueError, KeyError):
            flash("Verifica todos los campos del formulario.", "error")
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
                
            except Exception:
                flash("Error al guardar ingreso.", "error")
            finally:
                conn.close()
        else:
            flash("Error de conexión a la base de datos.", "error")
            
        return redirect(url_for('routes.formulario_ingreso_alimento'))

    return render_template('formulario_ingreso_alimento.html')

@bp.route('/formulario_muestreo', methods=['GET', 'POST'])
def formulario_muestreo():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))
        
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
            
        return redirect(url_for('routes.formulario_muestreo'))

    return render_template('formulario_muestreo.html')

@bp.route('/formulario_parametros', methods=['GET', 'POST'])
def formulario_parametros():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))
        
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
            
        return redirect(url_for('routes.formulario_parametros'))

    return render_template('formulario_parametros.html')

@bp.route('/formulario_siembra', methods=['GET', 'POST'])
def formulario_siembra():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))
    
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
            
        return redirect(url_for('routes.formulario_siembra'))

    return render_template('formulario_siembra.html')

@bp.route('/formulario_informes', methods=['GET', 'POST'])
def formulario_informes():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))
    
    resultados = []
    formulario_seleccionado = ''
    
    if request.method == 'POST':
        formulario = request.form.get('formulario', '').strip()
        formulario_seleccionado = formulario
        fecha_desde = request.form.get('fecha_desde', '').strip()
        fecha_hasta = request.form.get('fecha_hasta', '').strip()
        estanque = request.form.get('estanque', '').strip()
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                if formulario and formulario != "todos":
                    tablas_query = [formulario]
                else:
                    tablas_query = ['alimento', 'muestreo', 'parametros', 'siembra']
                    formulario_seleccionado = 'todos'
                
                for tabla in tablas_query:
                    try:
                        query = f"SELECT *, '{tabla}' as tipo FROM {tabla} WHERE 1=1"
                        params = []
                        
                        if fecha_desde:
                            query += " AND fecha >= ?"
                            params.append(fecha_desde)
                        
                        if fecha_hasta:
                            query += " AND fecha <= ?"
                            params.append(fecha_hasta)
                        
                        if estanque:
                            query += " AND estanque LIKE ?"
                            params.append(f"%{estanque}%")
                        
                        query += " ORDER BY fecha DESC"
                        
                        cursor.execute(query, params)
                        rows = cursor.fetchall()
                        
                        columns = [description[0] for description in cursor.description]
                        registros_tabla = [dict(zip(columns, row)) for row in rows]
                        
                        resultados.extend(registros_tabla)
                        
                    except Exception:
                        continue
                
                if resultados:
                    resultados.sort(key=lambda x: x.get('fecha', ''), reverse=True)
                
            except Exception:
                pass
            finally:
                conn.close()
    
    return render_template('formulario_informes_final.html', 
                         resultados=resultados, 
                         formulario_seleccionado=formulario_seleccionado)

@bp.route('/filtrar_informes')
def filtrar_informes():
    print("🔍 RUTA FILTRAR_INFORMES LLAMADA")
    print(f"📥 request.args: {dict(request.args)}")
    
    try:
        formulario = request.args.get('formulario')
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        estanque = request.args.get('estanque')
        
        print(f"📋 Parámetros: formulario={formulario}, fecha_inicio={fecha_inicio}, fecha_fin={fecha_fin}, estanque={estanque}")
        
        if not formulario:
            print("❌ No se especificó formulario")
            return jsonify({'success': False, 'message': 'Formulario no especificado'})
        
        # Construir la consulta base según el formulario
        if formulario == 'alimento':
            query = "SELECT fecha, estanque, tipo_alimento, cantidad_kg as cantidad, observaciones FROM alimento WHERE 1=1"
        elif formulario == 'muestreo':
            query = "SELECT fecha, estanque, peso_promedio, cantidad_peces, (peso_promedio * cantidad_peces / 1000) as biomasa, observaciones FROM muestreo WHERE 1=1"
        elif formulario == 'parametros':
            query = "SELECT fecha, estanque, temperatura, ph, oxigeno, observaciones FROM parametros WHERE 1=1"
        elif formulario == 'siembra':
            query = "SELECT fecha, estanque, especie, cantidad as cantidad_alevinos, peso_promedio, observaciones FROM siembra WHERE 1=1"
        else:
            print(f"❌ Formulario no válido: {formulario}")
            return jsonify({'success': False, 'message': f'Formulario no válido: {formulario}'})
        
        params = []
        
        # Agregar filtros opcionales
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
        
        print(f"🔍 Query: {query}")
        print(f"📋 Params: {params}")
        
        # Ejecutar consulta
        conn = get_db_connection()
        if not conn:
            print("❌ Error de conexión a la base de datos")
            return jsonify({'success': False, 'message': 'Error de conexión a la base de datos'})
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            # Obtener nombres de columnas
            columns = [description[0] for description in cursor.description]
            resultados = []
            
            for row in cursor.fetchall():
                resultado = dict(zip(columns, row))
                resultados.append(resultado)
            
            conn.close()
            
            print(f"✅ Consulta exitosa. Resultados: {len(resultados)}")
            
            return jsonify({
                'success': True,
                'datos': resultados,
                'total': len(resultados)
            })
            
        except Exception as e:
            conn.close()
            print(f"❌ Error en consulta: {str(e)}")
            return jsonify({'success': False, 'message': f'Error en consulta: {str(e)}'})
            
    except Exception as e:
        print(f"❌ Error interno: {str(e)}")
        return jsonify({'success': False, 'message': f'Error interno: {str(e)}'})

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.index'))
