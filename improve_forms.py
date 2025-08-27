#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mejorar todos los formularios con iconos de Font Awesome
"""

import os
import re

# Ruta base de los templates
TEMPLATES_DIR = "templates"

# Mapeo de archivos y sus títulos mejorados
FORM_UPDATES = {
    "formulario_ingreso_alimento.html": {
        "title_old": "Ingreso de Alimento - Piscícola Fish River",
        "title_new": "🍽️ Ingreso de Alimento - Piscícola Fish River",
        "form_title": "<i class=\"fas fa-plus-circle\"></i> Formulario de Ingreso de Alimento"
    },
    "formulario_muestreo.html": {
        "title_old": "Muestreo - Piscícola Fish River", 
        "title_new": "🔬 Muestreo - Piscícola Fish River",
        "form_title": "<i class=\"fas fa-microscope\"></i> Formulario de Muestreo"
    },
    "formulario_parametros.html": {
        "title_old": "Parámetros - Piscícola Fish River",
        "title_new": "⚙️ Parámetros - Piscícola Fish River", 
        "form_title": "<i class=\"fas fa-cogs\"></i> Formulario de Parámetros"
    },
    "formulario_siembra.html": {
        "title_old": "Siembra - Piscícola Fish River",
        "title_new": "🌱 Siembra - Piscícola Fish River",
        "form_title": "<i class=\"fas fa-seedling\"></i> Formulario de Siembra"
    }
}

# Iconos para campos comunes
FIELD_ICONS = {
    "fecha": "<i class=\"fas fa-calendar-alt\"></i>",
    "hora": "<i class=\"fas fa-clock\"></i>", 
    "frecuencia": "<i class=\"fas fa-clock\"></i>",
    "estanque": "<i class=\"fas fa-fish\"></i>",
    "cantidad": "<i class=\"fas fa-weight\"></i>",
    "peso": "<i class=\"fas fa-weight\"></i>",
    "temperatura": "<i class=\"fas fa-thermometer-half\"></i>",
    "oxigeno": "<i class=\"fas fa-wind\"></i>",
    "ph": "<i class=\"fas fa-flask\"></i>",
    "observaciones": "<i class=\"fas fa-comment\"></i>",
    "acciones": "<i class=\"fas fa-tools\"></i>"
}

def improve_form_file(file_path, form_config):
    """Mejora un archivo de formulario con iconos"""
    
    print(f"📝 Mejorando {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Agregar Font Awesome en el head si no existe
    if 'font-awesome' not in content:
        content = content.replace(
            '<head>',
            '<head>\n  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">'
        )
    
    # 2. Actualizar título de la página
    if form_config.get('title_old'):
        content = content.replace(
            f"<title>{form_config['title_old']}</title>",
            f"<title>{form_config['title_new']}</title>"
        )
    
    # 3. Mejorar header principal
    content = content.replace(
        '<h1>Piscícola Fish River</h1>',
        '<h1><i class="fas fa-fish"></i> Piscícola Fish River <i class="fas fa-water"></i></h1>'
    )
    
    # 4. Mejorar botón menú
    content = content.replace(
        'onclick="toggleMenu()">Menú</button>',
        'onclick="toggleMenu()"><i class="fas fa-bars"></i> Menú</button>'
    )
    
    # 5. Mejorar iconos del menú
    menu_replacements = [
        ('">🏠 Inicio</a>', '"><i class="fas fa-home"></i> Inicio</a>'),
        ('">📋 Formulario de Alimentos</a>', '"><i class="fas fa-utensils"></i> Formulario de Alimentos</a>'),
        ('">🍽️ Formulario de Ingreso de Alimento</a>', '"><i class="fas fa-plus-circle"></i> Formulario de Ingreso de Alimento</a>'),
        ('">🔬 Formulario de Muestreo</a>', '"><i class="fas fa-microscope"></i> Formulario de Muestreo</a>'),
        ('">⚙️ Formulario de Parámetros</a>', '"><i class="fas fa-cogs"></i> Formulario de Parámetros</a>'),
        ('">🌱 Formulario de Siembra</a>', '"><i class="fas fa-seedling"></i> Formulario de Siembra</a>'),
        ('">📊 Informes</a>', '"><i class="fas fa-chart-bar"></i> Informes</a>')
    ]
    
    for old, new in menu_replacements:
        content = content.replace(old, new)
    
    # 6. Actualizar título del formulario
    if form_config.get('form_title'):
        # Buscar patrones comunes de títulos
        patterns = [
            r'<h2[^>]*>Formulario de [^<]+</h2>',
            r'<h2[^>]*>[^<]*Formulario[^<]*</h2>'
        ]
        
        for pattern in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, f'<h2 class="titulo-form">{form_config["form_title"]}</h2>', content)
                break
    
    # 7. Agregar iconos a campos comunes
    for field, icon in FIELD_ICONS.items():
        # Buscar labels que contengan estas palabras
        patterns = [
            f'<label[^>]*>{field.title()}:',
            f'<label[^>]*>{field.title()} ',
            f'<label[^>]*>{field.lower()}:',
            f'<label[^>]*>{field.lower()} '
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(
                    pattern,
                    lambda m: m.group(0).replace(f'>{field.title()}:', f'>{icon} {field.title()}:').replace(f'>{field.lower()}:', f'>{icon} {field.title()}:'),
                    content,
                    flags=re.IGNORECASE
                )
    
    # Guardar archivo mejorado
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {file_path} mejorado correctamente")

def main():
    """Función principal"""
    print("🚀 Iniciando mejora de formularios con iconos Font Awesome\n")
    
    # Mejorar cada formulario
    for filename, config in FORM_UPDATES.items():
        file_path = os.path.join(TEMPLATES_DIR, filename)
        if os.path.exists(file_path):
            improve_form_file(file_path, config)
        else:
            print(f"❌ No se encontró: {file_path}")
    
    print("\n🎉 ¡Todos los formularios han sido mejorados con iconos!")
    print("📋 Cambios aplicados:")
    print("  • Iconos Font Awesome agregados")
    print("  • Títulos mejorados con emojis")
    print("  • Menús con iconos profesionales")
    print("  • Campos con iconos descriptivos")

if __name__ == "__main__":
    main()
