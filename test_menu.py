#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que los menús están funcionando correctamente
"""

def test_menu_consistency():
    """Verificar que todos los formularios tengan el mismo menú"""
    
    print("🧪 Verificando consistencia de menús entre formularios...\n")
    
    # Archivos a verificar
    files = [
        'templates/formulario_alimentos.html',
        'templates/formulario_ingreso_alimento.html', 
        'templates/formulario_muestreo.html'
    ]
    
    expected_menu_items = [
        'Formulario de Alimentos',
        'Formulario de Ingreso de Alimento',
        'Formulario de Muestreo',
        'Formulario de Parámetros',
        'Formulario de Siembra'
    ]
    
    for file_path in files:
        print(f"📋 Verificando {file_path}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Verificar elementos del menú
            missing_items = []
            for item in expected_menu_items:
                if item not in content:
                    missing_items.append(item)
            
            # Verificar función toggleMenu
            has_toggle_function = 'function toggleMenu()' in content
            
            # Verificar estructura del menú
            has_menu_structure = 'id="menu"' in content and 'class="menu-list"' in content
            
            # Mostrar resultados
            if not missing_items and has_toggle_function and has_menu_structure:
                print(f"   ✅ Menú completo y funcional")
            else:
                print(f"   ❌ Problemas encontrados:")
                if missing_items:
                    print(f"      - Faltan elementos: {', '.join(missing_items)}")
                if not has_toggle_function:
                    print(f"      - Falta función toggleMenu()")
                if not has_menu_structure:
                    print(f"      - Falta estructura del menú")
                    
        except FileNotFoundError:
            print(f"   ❌ Archivo no encontrado")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("✨ Verificación completada")

if __name__ == "__main__":
    test_menu_consistency()
