#!/usr/bin/env python3
"""
Aplicación Flask simplificada para diagnóstico
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'test_key_simple'

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
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/formulario_alimentos', methods=['GET', 'POST'])
def formulario_alimentos():
    print("🔍 ACCESO AL FORMULARIO DE ALIMENTOS")
    
    if not session.get('logged_in'):
        print("❌ Usuario no autenticado")
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        print("✅ POST RECIBIDO - Datos del formulario:")
        for key, value in request.form.items():
            print(f"   {key}: {value}")
        
        # Simular guardado exitoso
        flash("¡Formulario procesado correctamente! (MODO TEST)", "success")
        print("✅ Formulario procesado correctamente")
        return redirect(url_for('formulario_alimentos'))
    
    print("📄 Mostrando formulario (GET)")
    return render_template('formulario_alimentos.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("🚀 Iniciando aplicación de prueba...")
    app.run(debug=True, host='0.0.0.0', port=5000)
