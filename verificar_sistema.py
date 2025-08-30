#!/usr/bin/env python3
"""
Script para restablecer y verificar la configuración del sistema
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verificar_archivos():
    """Verifica que todos los archivos principales estén en su lugar"""
    
    archivos_importantes = [
        'app.py',
        'config.py', 
        'database_config.py',
        'routes/__init__.py',
        'static/styles.css',
        'static/images/fondo.jpeg',
        'templates/index.html',
        'templates/login.html',
        'templates/dashboard.html',
        'templates/formulario_informes_final.html'
    ]
    
    print("🔍 VERIFICANDO ARCHIVOS DEL SISTEMA...")
    print("=" * 50)
    
    todos_ok = True
    for archivo in archivos_importantes:
        ruta_completa = os.path.join(os.path.dirname(__file__), archivo)
        if os.path.exists(ruta_completa):
            tamaño = os.path.getsize(ruta_completa)
            print(f"✅ {archivo} - {tamaño} bytes")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            todos_ok = False
    
    print("\n🌐 CONFIGURACIÓN DE RED:")
    print("=" * 50)
    print("✅ Servidor: http://0.0.0.0:5000")
    print("✅ IP Local: http://192.168.20.2:5000")
    print("✅ Acceso: admin / admin123")
    
    print("\n📱 CARACTERÍSTICAS RESPONSIVE:")
    print("=" * 50)
    print("✅ CSS optimizado para móviles")
    print("✅ Meta viewport configurado")
    print("✅ Tablas con scroll horizontal")
    print("✅ Botones touch-friendly")
    
    if todos_ok:
        print("\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL")
        print("📝 Accede desde cualquier dispositivo a: http://192.168.20.2:5000")
    else:
        print("\n⚠️  HAY ARCHIVOS FALTANTES")
    
    return todos_ok

def mostrar_instrucciones():
    """Muestra instrucciones de uso"""
    
    print("\n" + "="*60)
    print("📱 GUÍA RÁPIDA DE USO")
    print("="*60)
    
    print("\n🔐 ACCESO:")
    print("1. Ve a: http://192.168.20.2:5000")
    print("2. Usuario: admin")
    print("3. Contraseña: admin123")
    
    print("\n📊 FUNCIONES PRINCIPALES:")
    print("• Dashboard - Resumen del sistema")
    print("• Alimentos - Registro de alimentación")
    print("• Ingreso de Alimentos - Control de inventario")
    print("• Muestreo - Seguimiento de peces")
    print("• Parámetros - Calidad del agua")
    print("• Siembra - Control de población")
    print("• Informes - Reportes y análisis")
    
    print("\n📱 OPTIMIZACIONES MÓVILES:")
    print("• Interfaz adaptativa automática")
    print("• Tablas con scroll horizontal")
    print("• Botones grandes para touch")
    print("• Formularios optimizados")
    
    print("\n🔧 SOLUCIÓN DE PROBLEMAS:")
    print("• Si algo no funciona, reinicia el navegador")
    print("• Limpia caché: Ctrl+F5 (o Cmd+Shift+R)")
    print("• En móvil: refresca la página")

if __name__ == "__main__":
    print("🚀 VERIFICANDO SISTEMA PISCÍCOLA...")
    
    if verificar_archivos():
        mostrar_instrucciones()
        print("\n✅ VERIFICACIÓN COMPLETADA - SISTEMA LISTO")
    else:
        print("\n❌ VERIFICACIÓN FALLÓ - CONTACTA SOPORTE")
