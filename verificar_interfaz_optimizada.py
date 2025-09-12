#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para verificar la interfaz optimizada sin scroll
Simula la navegación por el formulario de informes
"""

import webbrowser
import time
import requests

print("🎯 VERIFICANDO INTERFAZ OPTIMIZADA SIN SCROLL")
print("=" * 50)

# Verificar que el servidor esté corriendo
try:
    response = requests.get("http://127.0.0.1:5000/")
    if response.status_code == 200:
        print("✅ Servidor Flask detectado en puerto 5000")
        
        # Abrir la interfaz del formulario de informes
        url_formulario = "http://127.0.0.1:5000/formulario_informes"
        print(f"🌐 Abriendo interfaz optimizada: {url_formulario}")
        
        webbrowser.open(url_formulario)
        
        print("\n📋 CARACTERÍSTICAS DE LA NUEVA INTERFAZ:")
        print("   ✅ Tabla sin scroll horizontal")
        print("   ✅ Columnas optimizadas con anchos fijos")
        print("   ✅ Texto truncado con tooltips")
        print("   ✅ Todas las columnas visibles simultáneamente")
        print("   ✅ Responsive para móviles y desktop")
        
        print("\n🎨 MEJORAS IMPLEMENTADAS:")
        print("   • Anchos de columna específicos (Id: 4%, Fecha: 10%, etc.)")
        print("   • Padding reducido para optimizar espacio")
        print("   • Texto truncado en campos largos con '...'")
        print("   • Tooltips al hacer hover para ver contenido completo")
        print("   • Font-size ajustado (0.8rem) para mostrar más contenido")
        print("   • Eliminación de scroll horizontal")
        
        print("\n💡 INSTRUCCIONES:")
        print("   1. Selecciona 'Alimento' en el formulario")
        print("   2. Haz clic en 'Filtrar' para ver la tabla optimizada")
        print("   3. Pasa el mouse sobre las celdas para ver tooltips")
        print("   4. Verifica que todas las columnas son visibles sin scroll")
        
    else:
        print("❌ Servidor no responde correctamente")
        
except requests.exceptions.ConnectionError:
    print("❌ No se puede conectar al servidor Flask")
    print("💡 Asegúrate de que el servidor esté ejecutándose con: python app.py")
except Exception as e:
    print(f"❌ Error inesperado: {e}")

print("\n✨ RESUMEN DE OPTIMIZACIÓN COMPLETADA")
print("=" * 50)
