#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICACIÓN COMPLETA DE TODOS LOS FORMULARIOS
==============================================
Script para verificar que todos los formularios tienen el atributo 'action' correcto.
"""

import os
import re

def verificar_formularios():
    """Verifica que todos los formularios HTML tengan el atributo action correcto"""
    
    print("🔍 VERIFICACIÓN DE FORMULARIOS")
    print("=" * 50)
    
    # Directorio de templates
    templates_dir = "templates"
    
    # Formularios a verificar
    formularios = {
        "formulario_alimentos.html": "formulario_alimentos",
        "formulario_ingreso_alimento.html": "formulario_ingreso_alimento", 
        "formulario_muestreo.html": "formulario_muestreo",
        "formulario_parametros.html": "formulario_parametros",
        "formulario_siembra.html": "formulario_siembra",
        "formulario_informes_final.html": "formulario_informes"
    }
    
    resultados = {}
    
    for archivo, ruta_esperada in formularios.items():
        archivo_path = os.path.join(templates_dir, archivo)
        
        if not os.path.exists(archivo_path):
            print(f"❌ {archivo}: Archivo no encontrado")
            resultados[archivo] = "NO_ENCONTRADO"
            continue
            
        try:
            with open(archivo_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
                
            # Buscar formularios con method POST
            formularios_post = re.findall(r'<form[^>]*method=["\']POST["\'][^>]*>', contenido, re.IGNORECASE)
            
            if not formularios_post:
                print(f"⚠️  {archivo}: No se encontraron formularios POST")
                resultados[archivo] = "SIN_POST"
                continue
                
            # Verificar si tiene action con la ruta correcta
            tiene_action_correcto = False
            for form_tag in formularios_post:
                if f'action="{{{{ url_for(\'{ruta_esperada}\') }}}}"' in form_tag:
                    tiene_action_correcto = True
                    break
                    
            if tiene_action_correcto:
                print(f"✅ {archivo}: Formulario correcto")
                resultados[archivo] = "CORRECTO"
            else:
                print(f"❌ {archivo}: Falta action o es incorrecto")
                print(f"   📍 Ruta esperada: {ruta_esperada}")
                # Mostrar formularios encontrados
                for i, form_tag in enumerate(formularios_post):
                    print(f"   📝 Form {i+1}: {form_tag[:100]}...")
                resultados[archivo] = "INCORRECTO"
                
        except Exception as e:
            print(f"❌ {archivo}: Error al leer archivo - {e}")
            resultados[archivo] = "ERROR"
            
    print("\n" + "=" * 50)
    print("📊 RESUMEN")
    print("=" * 50)
    
    correctos = sum(1 for r in resultados.values() if r == "CORRECTO")
    total = len(formularios)
    
    print(f"✅ Formularios correctos: {correctos}/{total}")
    
    if correctos == total:
        print("🎉 ¡TODOS LOS FORMULARIOS ESTÁN CORRECTOS!")
    else:
        print("⚠️  Hay formularios que necesitan corrección")
        
    return resultados

def mostrar_ejemplo_correccion():
    """Muestra ejemplo de cómo corregir un formulario"""
    
    print("\n" + "=" * 50)
    print("💡 EJEMPLO DE CORRECCIÓN")
    print("=" * 50)
    
    print("❌ INCORRECTO:")
    print('<form method="POST" class="mi-form">')
    
    print("\n✅ CORRECTO:")
    print('<form action="{{ url_for(\'formulario_alimentos\') }}" method="POST" class="mi-form">')
    
    print("\n📝 NOTA: El action debe usar url_for() con el nombre exacto de la ruta en Flask")

if __name__ == "__main__":
    resultados = verificar_formularios()
    mostrar_ejemplo_correccion()
    
    # Si hay errores, mostrar código de salida 1
    if any(r != "CORRECTO" for r in resultados.values()):
        print("\n❗ Algunos formularios necesitan corrección")
        exit(1)
    else:
        print("\n🎉 Verificación completada exitosamente")
        exit(0)
