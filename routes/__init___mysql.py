from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
import datetime
import sys
import os

# Agregar el directorio raíz al path para importar database_config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_config import get_connection, init_db

bp = Blueprint('routes', __name__)

# ---------------------------------------
# Conexión a la base de datos (SQLite)
# ---------------------------------------
def get_db_connection():
    """
    Conexión SQLite para producción
    """
    try:
        conn = get_connection()
        print("✅ Conectado a la base de datos SQLite")
        return conn
    except Exception as e:
        print(f"❌ Error de conexión a base de datos: {e}")
        return None

# ---------------------------------------
# Ruta principal (índice)
# ---------------------------------------
@bp.route('/')
def index():
	return render_template('index.html')

# ---------------------------------------
# Login
# ---------------------------------------
@bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = request.form['username']
		pwd  = request.form['password']
		if user == 'admin' and pwd == '123456':
			session['logged_in'] = True
			return redirect(url_for('routes.dashboard'))
		flash("Usuario o contraseña incorrectos.", "error")
	return render_template('login.html')

# ---------------------------------------
# Dashboard
# ---------------------------------------
@bp.route('/dashboard')
def dashboard():
	if not session.get('logged_in'):
		return redirect(url_for('routes.login'))

	conn = get_db_connection()
	alimentos = []
	if conn:
		try:
			cur = conn.cursor()
			cur.execute("SELECT * FROM alimento ORDER BY fecha DESC")
			alimentos = cur.fetchall()
		except Exception as e:
			print(f"❌ Error al leer 'alimento': {e}")
		finally:
			conn.close()
	return render_template('dashboard.html', alimentos=alimentos)

# ---------------------------------------
# Formulario de Alimentos
# ---------------------------------------
@bp.route('/formulario_alimentos', methods=['GET', 'POST'])
def formulario_alimentos():
	if request.method == 'POST':
		try:
			fecha                = request.form['fecha']
			frecuencia_toma      = request.form['frecuencia_toma']
			estanque_celda       = request.form['estanque_celda']
			referencia_alimento  = request.form['referencia_alimento']
			cantidad_alimento    = float(request.form['cantidad_alimento'])
			mortalidad           = int(request.form['mortalidad'])
			causa_mortalidad     = request.form['causa_mortalidad']
			acciones_correctivas = request.form['acciones_correctivas']
		except ValueError as ve:
			flash("Verifica los campos numéricos.", "error")
			print(f"❌ Tipo: {ve}")
			return render_template('formulario_alimentos.html')

		if not all([fecha, frecuencia_toma, estanque_celda,
					referencia_alimento, causa_mortalidad, acciones_correctivas]):
			flash("Todos los campos son obligatorios.", "error")
			return render_template('formulario_alimentos.html')

		# Conectar y guardar en BD
		conn = get_db_connection()
		if conn:
			try:
				cur = conn.cursor()
				cur.execute('''
					INSERT INTO alimento (
						fecha, frecuencia_toma, estanque_celda, referencia_alimento,
						cantidad_alimento, mortalidad, causa_mortalidad, acciones_correctivas
					) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
				''', (
					fecha, frecuencia_toma, estanque_celda, referencia_alimento,
					cantidad_alimento, mortalidad, causa_mortalidad, acciones_correctivas
				))
				conn.commit()
				flash("Alimento guardado correctamente.", "success")
				print("✅ Datos insertados en tabla alimento")
			except Error as e:
				flash("Error al guardar en la BD.", "error")
				print(f"❌ SQL Alimento: {e}")
			finally:
				conn.close()
		else:
			flash("Error de conexión a la base de datos.", "error")
		
		return redirect(url_for('routes.formulario_alimentos'))

	return render_template('formulario_alimentos.html')

# ---------------------------------------
# Formulario de Ingreso de Alimento
# ---------------------------------------
@bp.route('/formulario_ingreso_alimento', methods=['GET', 'POST'])
def formulario_ingreso_alimento():
	if request.method == 'POST':
		try:
			fecha          = request.form['fecha']
			hora           = request.form['hora']
			ingreso_comida = request.form['ingreso_comida']
			cantidad       = float(request.form['cantidad'])
			transporte     = request.form['transporte']
			observaciones  = request.form.get('observaciones', '')
		except ValueError as ve:
			flash("Cantidad debe ser numérica.", "error")
			print(f"❌ Tipo: {ve}")
			return render_template('formulario_ingreso_alimento.html')

		if not all([fecha, hora, ingreso_comida, transporte]) or cantidad <= 0:
			flash("Campos obligatorios y cantidad > 0.", "error")
			return render_template('formulario_ingreso_alimento.html')

		conn = get_db_connection()
		if conn:
			try:
				cur = conn.cursor()
				cur.execute('''
					INSERT INTO ingreso_alimentos (
						fecha, hora, ingreso_comida, cantidad, transporte, observaciones
					) VALUES (%s,%s,%s,%s,%s,%s)
				''', (fecha, hora, ingreso_comida, cantidad, transporte, observaciones))
				conn.commit()
				flash("Ingreso guardado correctamente.", "success")
			except Error as e:
				flash("Error al guardar ingreso.", "error")
				print(f"❌ SQL Ingreso: {e}")
			finally:
				conn.close()
		else:
			flash("Error de conexión a la base de datos.", "error")
		return redirect(url_for('routes.formulario_ingreso_alimento'))

	return render_template('formulario_ingreso_alimento.html')

# ---------------------------------------
# Formulario de Muestreo
# ---------------------------------------
@bp.route('/formulario_muestreo', methods=['GET', 'POST'])
def formulario_muestreo():
	if request.method == 'POST':
		try:
			fecha             = request.form['fecha']
			frecuencia_toma   = request.form['frecuencia_toma']
			especie           = request.form['especie']
			biomasa           = float(request.form['biomasa'])
			estanque_celda    = request.form['estanque_celda']
			peces             = int(request.form['peces'])
			peso_promedio_g   = float(request.form['peso_promedio_g'])
			promedio_total_g  = float(request.form['promedio_total_g'])
			acciones_corr     = request.form['acciones_correctivas']
		except ValueError as ve:
			flash("Verifica campos numéricos de muestreo.", "error")
			print(f"❌ Tipo: {ve}")
			return render_template('formulario_muestreo.html')

		if (not all([fecha, frecuencia_toma, especie, estanque_celda, acciones_corr]) or
			biomasa <= 0 or peces < 0 or peso_promedio_g <= 0 or promedio_total_g <= 0):
			flash("Campos obligatorios y valores > 0.", "error")
			return render_template('formulario_muestreo.html')

		conn = get_db_connection()
		if conn:
			try:
				cur = conn.cursor()
				cur.execute('''
					INSERT INTO muestreo (
						fecha, frecuencia_toma, especie, biomasa,
						estanque_celda, peces, peso_promedio_g,
						promedio_total_g, acciones_correctivas
					) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
				''', (
					fecha, frecuencia_toma, especie, biomasa,
					estanque_celda, peces, peso_promedio_g,
					promedio_total_g, acciones_corr
				))
				conn.commit()
				flash("Muestreo registrado correctamente.", "success")
			except Error as e:
				flash("Error al guardar muestreo.", "error")
				print(f"❌ SQL Muestreo: {e}")
			finally:
				conn.close()
		else:
			flash("Error de conexión a la base de datos.", "error")
		return redirect(url_for('routes.formulario_muestreo'))

	return render_template('formulario_muestreo.html')

# ---------------------------------------
# FORMULARIO DE PARÁMETROS
# ---------------------------------------
@bp.route('/formulario_parametros', methods=['GET', 'POST'])
def formulario_parametros():
	if request.method == 'POST':
		# Capturar datos del formulario
		fecha = request.form.get('fecha')
		hora = request.form.get('hora')
		estanque_celda = request.form.get('estanque_celda')
		oxigeno = request.form.get('oxigeno')
		temperatura = request.form.get('temperatura')
		ph = request.form.get('ph')
		amonio = request.form.get('amonio')
		observaciones = request.form.get('observaciones')
		
		# Conectar y guardar en BD
		conn = get_db_connection()
		if conn:
			try:
				cur = conn.cursor()
				cur.execute('''
					INSERT INTO parametros (
						fecha, hora, estanque_celda, oxigeno,
						temperatura, ph, amonio, observaciones
					) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
				''', (
					fecha, hora, estanque_celda, oxigeno,
					temperatura, ph, amonio, observaciones
				))
				conn.commit()
				flash("Parámetros registrados correctamente.", "success")
			except Error as e:
				flash("Error al guardar parámetros.", "error")
				print(f"❌ SQL Parámetros: {e}")
			finally:
				conn.close()
		else:
			flash("Error de conexión a la base de datos.", "error")
		return redirect(url_for('routes.formulario_parametros'))

	return render_template('formulario_parametros.html')

# ---------------------------------------
# Formulario de Siembra
# ---------------------------------------
@bp.route('/formulario_siembra', methods=['GET', 'POST'])
def formulario_siembra():
	if not session.get('logged_in'):
		return redirect(url_for('routes.login'))
	
	if request.method == 'POST':
		# Obtener datos del formulario
		frecuencia_toma = request.form['frecuencia_toma']
		fecha = request.form['fecha']
		hora_siembra = request.form['hora_siembra']
		origen_semilla = request.form['origen_semilla']
		codigo_trazabilidad = request.form['codigo_trazabilidad']
		especie = request.form['especie']
		destino = request.form['destino']
		hembras_machos = request.form['hembras_machos']
		ovas_alevinos = request.form['ovas_alevinos']
		peso_promedio = request.form['peso_promedio']
		biomasa = request.form['biomasa']
		estanque_celda = request.form['estanque_celda']
		acciones_correctivas = request.form['acciones_correctivas']
		
		# Guardar en la base de datos
		conn = get_db_connection()
		if conn:
			try:
				cursor = conn.cursor()
				cursor.execute("""
					INSERT INTO siembra (
						frecuencia_toma, fecha, hora_siembra, origen_semilla,
						codigo_trazabilidad, especie, destino, hembras_machos,
						ovas_alevinos, peso_promedio, biomasa, estanque_celda,
						acciones_correctivas
					) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
				""", (
					frecuencia_toma, fecha, hora_siembra, origen_semilla,
					codigo_trazabilidad, especie, destino, hembras_machos,
					ovas_alevinos, peso_promedio, biomasa, estanque_celda,
					acciones_correctivas
				))
				conn.commit()
				flash("Datos de siembra registrados correctamente.", "success")
			except Error as e:
				flash("Error al guardar los datos de siembra.", "error")
				print(f"❌ SQL Siembra: {e}")
			finally:
				conn.close()
		else:
			flash("Error de conexión a la base de datos.", "error")
		return redirect(url_for('routes.formulario_siembra'))

	return render_template('formulario_siembra.html')

# ---------------------------------------
# Formulario de Informes
# ---------------------------------------
@bp.route('/formulario_informes', methods=['GET', 'POST'])
def formulario_informes():
	if not session.get('logged_in'):
		return redirect(url_for('routes.login'))
	
	resultados = []
	formulario_seleccionado = ''
	
	# Obtener filtros del formulario
	if request.method == 'POST':
		formulario = request.form.get('formulario', '').strip()
		formulario_seleccionado = formulario
		fecha_desde = request.form.get('fecha_desde', '').strip()
		fecha_hasta = request.form.get('fecha_hasta', '').strip()
		estanque = request.form.get('estanque', '').strip()
		
		conn = get_db_connection()
		if conn:
			try:
				cursor = conn.cursor(dictionary=True)
				
				# Determinar qué tabla consultar
				if formulario and formulario.strip() != "" and formulario.strip() != "todos":
					tablas_query = [formulario]
				else:
					tablas_query = ['alimento', 'ingreso_alimentos', 'muestreo', 'parametros', 'siembra']
					formulario_seleccionado = 'todos'
				
				for tabla in tablas_query:
					try:
						# Construir la consulta base
						query = f"SELECT *, '{tabla}' as tipo FROM {tabla} WHERE 1=1"
						params = []
						
						# Agregar filtros de fecha
						if fecha_desde:
							query += " AND fecha >= %s"
							params.append(fecha_desde)
						
						if fecha_hasta:
							query += " AND fecha <= %s"
							params.append(fecha_hasta)
						
						# Agregar filtro de estanque (solo para tablas que lo tienen)
						if estanque and tabla in ['alimento', 'muestreo', 'parametros', 'siembra']:
							query += " AND estanque_celda LIKE %s"
							params.append(f"%{estanque}%")
						
						# Ordenar por fecha descendente (más reciente primero)
						query += " ORDER BY fecha DESC"
						
						cursor.execute(query, params)
						registros_tabla = cursor.fetchall()
						
						resultados.extend(registros_tabla)
						
					except Exception as e:
						continue
				
				# Ordenar todos los resultados por fecha descendente (más reciente primero)
				if resultados:
					resultados.sort(key=lambda x: x.get('fecha') if x.get('fecha') else datetime.date.min, reverse=True)
				
			except Exception as e:
				pass
			finally:
				if conn.is_connected():
					cursor.close()
					conn.close()
	
	return render_template('formulario_informes_final.html', 
	                       resultados=resultados, 
	                       formulario_seleccionado=formulario_seleccionado)