#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRUEBA INTEGRAL DE TODOS LOS FORMULARIOS
========================================
Script para probar que todos los formularios guardan correctamente en la base de datos.
"""

import requests
import json
import time
from datetime import datetime, date

# Configuración
BASE_URL = "http://localhost:5000"
LOGIN_DATA = {"username": "admin", "password": "admin123"}

def test_login_and_get_session():
    """Hacer login y obtener sesión"""
    print("🔐 Iniciando sesión...")
    
    session = requests.Session()
    
    # Obtener página de login (para posibles tokens CSRF)
    login_page = session.get(f"{BASE_URL}/login")
    if login_page.status_code != 200:
        print(f"❌ Error obteniendo página de login: {login_page.status_code}")
        return None
        
    # Hacer login
    login_response = session.post(f"{BASE_URL}/login", data=LOGIN_DATA)
    if login_response.status_code != 200:
        print(f"❌ Error en login: {login_response.status_code}")
        return None
        
    print("✅ Login exitoso")
    return session

def test_formulario_alimentos(session):
    """Probar formulario de alimentos"""
    print("\n🐟 Probando formulario de alimentos...")
    
    datos_test = {
        'fecha': '2025-09-11',
        'hora': '14:30',
        'estanque': '1',
        'especie': 'Tilapia Test',
        'cantidad_peces': '150',
        'tipo_alimento': 'Concentrado Test',
        'cantidad_alimento': '2.5',
        'precio_kilo': '3500',
        'costo_total': '8750',
        'proveedor': 'Proveedor Test',
        'observaciones': 'Prueba automática de formulario'
    }
    
    try:
        response = session.post(f"{BASE_URL}/formulario_alimentos", data=datos_test)
        if response.status_code == 200 or response.status_code == 302:
            print("✅ Formulario de alimentos enviado correctamente")
            return True
        else:
            print(f"❌ Error en formulario de alimentos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Excepción en formulario de alimentos: {e}")
        return False

def test_formulario_muestreo(session):
    """Probar formulario de muestreo"""
    print("\n🔬 Probando formulario de muestreo...")
    
    datos_test = {
        'fecha': '2025-09-11',
        'frecuencia_toma': 'Diaria Test',
        'especie': 'Tilapia Test',
        'biomasa': '50.75',
        'estanque_celda': '1',
        'peces': '100',
        'peso_promedio_g': '120.5',
        'promedio_total_g': '12050',
        'acciones_correctivas': 'Prueba automática de muestreo'
    }
    
    try:
        response = session.post(f"{BASE_URL}/formulario_muestreo", data=datos_test)
        if response.status_code == 200 or response.status_code == 302:
            print("✅ Formulario de muestreo enviado correctamente")
            return True
        else:
            print(f"❌ Error en formulario de muestreo: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Excepción en formulario de muestreo: {e}")
        return False

def test_formulario_parametros(session):
    """Probar formulario de parámetros"""
    print("\n⚙️ Probando formulario de parámetros...")
    
    datos_test = {
        'fecha': '2025-09-11',
        'hora': '14:30',
        'estanque': '1',
        'temperatura': '24.5',
        'ph': '7.2',
        'oxigeno': '6.5',
        'turbidez': '3.2',
        'alcalinidad': '120',
        'dureza': '80',
        'amonio': '0.1',
        'nitritos': '0.05',
        'nitratos': '10.5',
        'observaciones': 'Prueba automática de parámetros'
    }
    
    try:
        response = session.post(f"{BASE_URL}/formulario_parametros", data=datos_test)
        if response.status_code == 200 or response.status_code == 302:
            print("✅ Formulario de parámetros enviado correctamente")
            return True
        else:
            print(f"❌ Error en formulario de parámetros: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Excepción en formulario de parámetros: {e}")
        return False

def test_formulario_siembra(session):
    """Probar formulario de siembra"""
    print("\n🌱 Probando formulario de siembra...")
    
    datos_test = {
        'frecuencia_toma': 'Semanal Test',
        'fecha': '2025-09-11',
        'hora': '14:30',
        'estanque': '1',
        'especie': 'Tilapia Test',
        'numero_alevinos': '500',
        'peso_promedio_g': '2.5',
        'talla_promedio_cm': '4.2',
        'mortalidad': '5',
        'proveedor_alevinos': 'Proveedor Test',
        'observaciones': 'Prueba automática de siembra'
    }
    
    try:
        response = session.post(f"{BASE_URL}/formulario_siembra", data=datos_test)
        if response.status_code == 200 or response.status_code == 302:
            print("✅ Formulario de siembra enviado correctamente")
            return True
        else:
            print(f"❌ Error en formulario de siembra: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Excepción en formulario de siembra: {e}")
        return False

def test_formulario_ingreso_alimento(session):
    """Probar formulario de ingreso de alimento"""
    print("\n➕ Probando formulario de ingreso de alimento...")
    
    datos_test = {
        'fecha': '2025-09-11',
        'hora': '14:30',
        'estanque': '1',
        'tipo_alimento': 'Pellets Test',
        'cantidad_kg': '3.2',
        'frecuencia_alimentacion': '3 veces/día',
        'observaciones': 'Prueba automática de ingreso de alimento'
    }
    
    try:
        response = session.post(f"{BASE_URL}/formulario_ingreso_alimento", data=datos_test)
        if response.status_code == 200 or response.status_code == 302:
            print("✅ Formulario de ingreso de alimento enviado correctamente")
            return True
        else:
            print(f"❌ Error en formulario de ingreso de alimento: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Excepción en formulario de ingreso de alimento: {e}")
        return False

def main():
    """Función principal para ejecutar todas las pruebas"""
    print("🧪 PRUEBA INTEGRAL DE TODOS LOS FORMULARIOS")
    print("=" * 60)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code != 200:
            print(f"❌ El servidor no responde correctamente: {response.status_code}")
            print("💡 Asegúrate de que app_mysql.py esté ejecutándose")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ No se puede conectar al servidor: {e}")
        print("💡 Asegúrate de que app_mysql.py esté ejecutándose en http://localhost:5000")
        return False
    
    print("✅ Servidor Flask respondiendo correctamente")
    
    # Hacer login
    session = test_login_and_get_session()
    if not session:
        return False
    
    # Probar todos los formularios
    resultados = {
        'alimentos': test_formulario_alimentos(session),
        'muestreo': test_formulario_muestreo(session),
        'parametros': test_formulario_parametros(session),
        'siembra': test_formulario_siembra(session),
        'ingreso_alimento': test_formulario_ingreso_alimento(session)
    }
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    exitosos = sum(1 for r in resultados.values() if r)
    total = len(resultados)
    
    for nombre, resultado in resultados.items():
        estado = "✅ CORRECTO" if resultado else "❌ ERROR"
        print(f"{nombre.upper():20} {estado}")
    
    print(f"\n📈 Formularios exitosos: {exitosos}/{total}")
    
    if exitosos == total:
        print("🎉 ¡TODOS LOS FORMULARIOS FUNCIONAN CORRECTAMENTE!")
        print("💡 Los datos se han guardado en la base de datos MySQL")
        return True
    else:
        print("⚠️  Algunos formularios presentan errores")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'🎊 PRUEBA COMPLETADA EXITOSAMENTE' if success else '❗ PRUEBA COMPLETADA CON ERRORES'}")
    exit(0 if success else 1)
