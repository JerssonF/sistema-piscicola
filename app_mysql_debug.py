#!/usr/bin/env python3
"""
Crear versión con logging detallado de app_mysql.py para debug
"""
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database_config_mysql import get_mysql_connection
from mysql.connector import Error
from datetime import datetime
import logging

# Configurar logging detallado
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'piscicola_secret_key_2025'

@app.route('/')
def home():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            logger.info(f"Login exitoso para usuario: {username}")
            return redirect(url_for('dashboard'))
        else:
            logger.warning(f"Intento de login fallido para usuario: {username}")
            flash('Credenciales incorrectas', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    logger.info("Usuario ha cerrado sesión")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/formulario_alimentos', methods=['GET', 'POST'])
def formulario_alimentos():
    logger.info("=== INICIO PROCESAMIENTO FORMULARIO ALIMENTOS ===")
    
    if not session.get('logged_in'):
        logger.warning("Usuario no autenticado intentando acceder al formulario")
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        logger.info("Método POST detectado - procesando formulario")
        
        try:
            # Log de todos los datos recibidos
            logger.info("Datos del formulario recibidos:")
            for key, value in request.form.items():
                logger.info(f"  {key}: {value}")
            
            # Campos básicos
            fecha = request.form['fecha']
            hora = request.form.get('hora', datetime.now().strftime('%H:%M'))
            estanque = request.form['estanque_celda']
            tipo_alimento = request.form['referencia_alimento']
            cantidad = float(request.form['cantidad_alimento'])
            
            logger.info(f"Campos procesados:")
            logger.info(f"  fecha: {fecha}")
            logger.info(f"  hora: {hora}")
            logger.info(f"  estanque: {estanque}")
            logger.info(f"  tipo_alimento: {tipo_alimento}")
            logger.info(f"  cantidad: {cantidad}")
            
            # Campos adicionales del template
            frecuencia_toma = request.form.get('frecuencia_toma', '')
            mortalidad = int(request.form.get('mortalidad', 0))
            causa_mortalidad = request.form.get('causa_mortalidad', '')
            acciones_correctivas = request.form.get('acciones_correctivas', '')
            
            logger.info(f"Campos adicionales:")
            logger.info(f"  frecuencia_toma: {frecuencia_toma}")
            logger.info(f"  mortalidad: {mortalidad}")
            logger.info(f"  causa_mortalidad: {causa_mortalidad}")
            logger.info(f"  acciones_correctivas: {acciones_correctivas}")
            
            # Crear observaciones combinando los campos adicionales
            observaciones = f"Frecuencia: {frecuencia_toma}; Mortalidad: {mortalidad}; Causa: {causa_mortalidad}; Acciones: {acciones_correctivas}"
            logger.info(f"Observaciones generadas: {observaciones}")
            
        except (ValueError, KeyError) as e:
            logger.error(f"Error procesando datos del formulario: {e}")
            flash(f"Error en los datos del formulario: {e}", "error")
            return render_template('formulario_alimentos.html')

        logger.info("Intentando conectar a la base de datos...")
        conn = get_mysql_connection()
        
        if conn:
            logger.info("✅ Conexión a base de datos establecida")
            try:
                cursor = conn.cursor()
                logger.info("✅ Cursor creado")
                
                consulta_sql = '''
                    INSERT INTO alimento (fecha, hora, estanque, tipo_alimento, cantidad_kg, observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                
                datos = (fecha, hora, estanque, tipo_alimento, cantidad, observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas)
                
                logger.info(f"Ejecutando consulta SQL:")
                logger.info(f"  SQL: {consulta_sql}")
                logger.info(f"  Datos: {datos}")
                
                cursor.execute(consulta_sql, datos)
                logger.info("✅ Consulta SQL ejecutada")
                
                conn.commit()
                logger.info("✅ Commit realizado exitosamente")
                
                # Verificar que se insertó
                cursor.execute("SELECT LAST_INSERT_ID()")
                last_id = cursor.fetchone()[0]
                logger.info(f"✅ Registro insertado con ID: {last_id}")
                
                flash("Alimento guardado correctamente.", "success")
                logger.info("✅ Mensaje de éxito enviado al usuario")
                
            except Error as e:
                logger.error(f"❌ Error MySQL al guardar: {e}")
                flash(f"Error al guardar en la base de datos: {e}", "error")
            except Exception as e:
                logger.error(f"❌ Error inesperado: {e}")
                flash(f"Error inesperado: {e}", "error")
            finally:
                if cursor:
                    cursor.close()
                    logger.info("Cursor cerrado")
                if conn.is_connected():
                    conn.close()
                    logger.info("Conexión cerrada")
        else:
            logger.error("❌ No se pudo establecer conexión a la base de datos")
            flash("Error de conexión a la base de datos.", "error")
        
        logger.info("Redirigiendo a formulario_alimentos")
        logger.info("=== FIN PROCESAMIENTO FORMULARIO ALIMENTOS ===")
        return redirect(url_for('formulario_alimentos'))

    logger.info("Método GET - mostrando formulario")
    return render_template('formulario_alimentos.html')

def get_db_connection():
    """Función de compatibilidad"""
    return get_mysql_connection()

if __name__ == '__main__':
    from database_config_mysql import create_database, init_mysql_tables
    create_database()
    init_mysql_tables()
    logger.info("🚀 Iniciando aplicación con logging detallado")
    app.run(debug=True, host='0.0.0.0', port=5000)
