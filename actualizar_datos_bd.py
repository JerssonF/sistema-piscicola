#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def actualizar_datos_bd():
    """Actualiza la base de datos local con los datos de phpMyAdmin"""
    
    print("🔄 ACTUALIZANDO BASE DE DATOS LOCAL")
    print("=" * 50)
    
    # Datos reales de phpMyAdmin
    datos_reales = [
        {
            'fecha': '2025-08-26',
            'mortalidad': 2,
            'causa_mortalidad': 'Enfermedad',
            'acciones_correctivas': 'Aumentar oxigenación'
        },
        {
            'fecha': '2025-08-25',
            'mortalidad': 0,
            'causa_mortalidad': '',
            'acciones_correctivas': 'Mantener rutina'
        },
        {
            'fecha': '2025-08-24',
            'mortalidad': 1,
            'causa_mortalidad': 'Estrés',
            'acciones_correctivas': 'Revisar temperatura'
        },
        {
            'fecha': '2025-08-21',
            'mortalidad': 56456,
            'causa_mortalidad': 'sadsd',
            'acciones_correctivas': 'dvcxv'
        },
        {
            'fecha': '2025-08-07',
            'mortalidad': 4,
            'causa_mortalidad': 'sdfdsd',
            'acciones_correctivas': 'aza'
        },
        {
            'fecha': '2025-08-14',
            'mortalidad': 4,
            'causa_mortalidad': 'asadsdsf',
            'acciones_correctivas': 'dfsdsfdsfds'
        }
    ]
    
    # Agregar registro que aparece en phpMyAdmin pero no en local
    datos_reales.append({
        'fecha': '2025-08-30',
        'hora': '08:00:00',
        'estanque': '1',
        'tipo_alimento': 'Premium',
        'cantidad_kg': 1.20,
        'observaciones': 'Diaria',
        'frecuencia_toma': 'Diaria',
        'mortalidad': 1200,
        'causa_mortalidad': 'Estres',
        'acciones_correctivas': 'Ampliar lago'
    })
    
    conn = sqlite3.connect('piscicola.db')
    cursor = conn.cursor()
    
    print("1️⃣ ACTUALIZANDO REGISTROS EXISTENTES:")
    
    for dato in datos_reales[:-1]:  # Todos excepto el último que se insertará
        print(f"\n   📄 Actualizando {dato['fecha']}...")
        
        # Verificar si existe
        cursor.execute("SELECT id FROM alimento WHERE fecha = ?", (dato['fecha'],))
        resultado = cursor.fetchone()
        
        if resultado:
            # Actualizar registro existente
            cursor.execute("""
                UPDATE alimento 
                SET mortalidad = ?, 
                    causa_mortalidad = ?, 
                    acciones_correctivas = ?
                WHERE fecha = ?
            """, (dato['mortalidad'], dato['causa_mortalidad'], 
                  dato['acciones_correctivas'], dato['fecha']))
            
            print(f"      ✅ Actualizado: mort={dato['mortalidad']}, causa='{dato['causa_mortalidad']}', acciones='{dato['acciones_correctivas']}'")
        else:
            print(f"      ❌ No encontrado registro para {dato['fecha']}")
    
    print(f"\n2️⃣ INSERTANDO REGISTRO NUEVO (2025-08-30):")
    
    nuevo_registro = datos_reales[-1]
    cursor.execute("""
        INSERT INTO alimento (
            fecha, hora, estanque, tipo_alimento, cantidad_kg, 
            observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nuevo_registro['fecha'],
        nuevo_registro['hora'],
        nuevo_registro['estanque'],
        nuevo_registro['tipo_alimento'],
        nuevo_registro['cantidad_kg'],
        nuevo_registro['observaciones'],
        nuevo_registro['frecuencia_toma'],
        nuevo_registro['mortalidad'],
        nuevo_registro['causa_mortalidad'],
        nuevo_registro['acciones_correctivas']
    ))
    
    print(f"   ✅ Insertado nuevo registro: {nuevo_registro['fecha']} con mortalidad={nuevo_registro['mortalidad']}")
    
    conn.commit()
    
    print(f"\n3️⃣ VERIFICANDO ACTUALIZACIONES:")
    
    cursor.execute("""
        SELECT fecha, mortalidad, causa_mortalidad, acciones_correctivas 
        FROM alimento 
        WHERE mortalidad > 0 OR causa_mortalidad != 'N/A' OR acciones_correctivas != 'Ninguna'
        ORDER BY fecha DESC
    """)
    
    registros_actualizados = cursor.fetchall()
    
    print(f"   📊 Registros con datos de mortalidad significativos: {len(registros_actualizados)}")
    
    for reg in registros_actualizados:
        fecha, mort, causa, acciones = reg
        print(f"      📄 {fecha}: mortalidad={mort}, causa='{causa}', acciones='{acciones}'")
    
    conn.close()
    
    print(f"\n✅ ACTUALIZACIÓN COMPLETADA")
    print(f"   📋 Ahora la BD local debería coincidir con phpMyAdmin")
    print(f"   🔄 Reinicia el servidor Flask para ver los cambios")

if __name__ == "__main__":
    actualizar_datos_bd()
