#!/usr/bin/env python3
"""
Script para actualizar y sincronizar TODOS los formularios con datos completos
que coincidan exactamente con la estructura de phpMyAdmin
"""

import sqlite3
import os
from datetime import datetime, timedelta
import random

def actualizar_todos_formularios():
    """Actualizar todas las tablas con datos completos y reales"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'piscicola.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("=" * 70)
        print("🔄 ACTUALIZANDO TODOS LOS FORMULARIOS CON DATOS COMPLETOS")
        print("=" * 70)
        
        # ======== TABLA ALIMENTO ========
        print("\n📋 ACTUALIZANDO TABLA ALIMENTO...")
        
        # Limpiar datos existentes
        cursor.execute("DELETE FROM alimento")
        
        # Datos completos de alimento con todas las columnas
        alimentos_completos = [
            ('2025-08-20', '08:00', '1', 'Pellet Premium 4mm', 15.5, 'Alimentación matutina normal', '3 veces al día', 2, 'Enfermedad bacteriana', 'Aumentar oxigenación y medicamento'),
            ('2025-08-21', '08:30', '2', 'Concentrado especial', 20.0, 'Alimentación vespertina', '2 veces al día', 0, '', 'Mantener rutina actual'),
            ('2025-08-22', '09:00', '1', 'Pellet crecimiento', 18.75, 'Incremento por crecimiento', '3 veces al día', 1, 'Estrés por temperatura', 'Revisar temperatura del agua'),
            ('2025-08-23', '07:45', '3', 'Alimento flotante', 12.5, 'Primera alimentación', '2 veces al día', 0, '', 'Todo normal'),
            ('2025-08-24', '08:15', '2', 'Pellet Premium 6mm', 22.0, 'Alimentación regular', '3 veces al día', 3, 'Problemas digestivos', 'Reducir cantidad temporalmente'),
            ('2025-08-25', '09:30', '1', 'Concentrado proteico', 16.8, 'Alimentación especial', '2 veces al día', 56456, 'Evento masivo', 'Investigar causa urgentemente'),
            ('2025-08-26', '08:00', '3', 'Pellet juvenil', 19.2, 'Alimentación matutina', '3 veces al día', 4, 'Calidad del agua', 'Cambio parcial de agua'),
            ('2025-08-27', '07:30', '2', 'Alimento medicado', 14.5, 'Tratamiento preventivo', '2 veces al día', 4, 'Parásitos', 'Continuar medicación 3 días'),
            ('2025-08-28', '08:45', '1', 'Pellet Premium 4mm', 21.3, 'Alimentación normal', '3 veces al día', 1200, 'Shock térmico', 'Estabilizar temperatura gradualmente')
        ]
        
        cursor.executemany('''
            INSERT INTO alimento (fecha, hora, estanque, tipo_alimento, cantidad_kg, observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', alimentos_completos)
        
        print(f"   ✅ Insertados {len(alimentos_completos)} registros de alimento")
        
        # ======== TABLA MUESTREO ========
        print("\n📋 ACTUALIZANDO TABLA MUESTREO...")
        
        cursor.execute("DELETE FROM muestreo")
        
        # Datos completos de muestreo
        muestreos_completos = [
            ('2025-08-20', '10:00', '1', 150.5, 12.3, 100, 'Crecimiento normal', 'Semanal', 'Tilapia', 15.05, 100),
            ('2025-08-21', '10:30', '2', 175.2, 13.1, 85, 'Buen desarrollo', 'Semanal', 'Cachama', 14.89, 85),
            ('2025-08-22', '11:00', '3', 145.8, 12.0, 95, 'Peso promedio en aumento', 'Semanal', 'Trucha', 13.85, 95),
            ('2025-08-23', '09:45', '1', 162.3, 12.8, 98, 'Excelente crecimiento', 'Semanal', 'Tilapia', 15.91, 98),
            ('2025-08-24', '10:15', '2', 180.5, 13.5, 82, 'Desarrollo óptimo', 'Semanal', 'Cachama', 14.80, 82),
            ('2025-08-25', '11:30', '3', 155.2, 12.4, 88, 'Crecimiento constante', 'Semanal', 'Trucha', 13.66, 88),
            ('2025-08-26', '09:30', '1', 168.7, 13.2, 96, 'Muy buen peso', 'Semanal', 'Tilapia', 16.20, 96),
            ('2025-08-27', '10:45', '2', 185.3, 14.0, 80, 'Peso excelente', 'Semanal', 'Cachama', 14.82, 80)
        ]
        
        cursor.executemany('''
            INSERT INTO muestreo (fecha, hora, estanque, peso_promedio, talla_promedio, cantidad_peces, observaciones, frecuencia_toma, especie, biomasa, peces)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', muestreos_completos)
        
        print(f"   ✅ Insertados {len(muestreos_completos)} registros de muestreo")
        
        # ======== TABLA PARAMETROS ========
        print("\n📋 ACTUALIZANDO TABLA PARAMETROS...")
        
        cursor.execute("DELETE FROM parametros")
        
        # Datos completos de parámetros
        parametros_completos = [
            ('2025-08-20', '07:00', '1', 24.5, 7.2, 6.8, 0.1, 0.05, 0.2, 'Parámetros óptimos', 'Diario', 6.8, 0.05),
            ('2025-08-20', '07:15', '2', 25.0, 7.0, 6.5, 0.15, 0.08, 0.25, 'Dentro del rango', 'Diario', 6.5, 0.08),
            ('2025-08-20', '07:30', '3', 24.8, 7.1, 6.7, 0.12, 0.06, 0.22, 'Buenos parámetros', 'Diario', 6.7, 0.06),
            ('2025-08-21', '07:00', '1', 24.2, 7.3, 6.9, 0.08, 0.04, 0.18, 'Excelente calidad', 'Diario', 6.9, 0.04),
            ('2025-08-21', '07:15', '2', 25.2, 6.9, 6.4, 0.18, 0.09, 0.28, 'Ajustar pH', 'Diario', 6.4, 0.09),
            ('2025-08-22', '07:00', '1', 24.7, 7.2, 6.8, 0.11, 0.05, 0.21, 'Valores estables', 'Diario', 6.8, 0.05),
            ('2025-08-22', '07:15', '2', 24.9, 7.1, 6.6, 0.14, 0.07, 0.24, 'Todo correcto', 'Diario', 6.6, 0.07),
            ('2025-08-23', '07:00', '3', 24.6, 7.0, 6.5, 0.13, 0.06, 0.23, 'Monitorear pH', 'Diario', 6.5, 0.06)
        ]
        
        cursor.executemany('''
            INSERT INTO parametros (fecha, hora, estanque, temperatura, ph, oxigeno, amonio, nitrito, nitrato, observaciones, frecuencia_toma, oxigeno_disuelto, nitritos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', parametros_completos)
        
        print(f"   ✅ Insertados {len(parametros_completos)} registros de parámetros")
        
        # ======== TABLA SIEMBRA ========
        print("\n📋 ACTUALIZANDO TABLA SIEMBRA...")
        
        cursor.execute("DELETE FROM siembra")
        
        # Datos completos de siembra
        siembras_completas = [
            ('2025-08-15', '08:00', '1', 'Tilapia', 1000, 0.5, 'Proveedor Local', 'Siembra inicial exitosa', 'Estanque comercial', 1000, 'Mixto 50/50'),
            ('2025-08-16', '09:00', '2', 'Cachama', 800, 0.8, 'Acuícola del Norte', 'Segunda siembra planificada', 'Estanque producción', 800, 'Mixto 60/40'),
            ('2025-08-17', '10:00', '3', 'Trucha', 600, 1.2, 'Truchas Andinas', 'Siembra de prueba', 'Estanque experimental', 600, 'Mixto 45/55'),
            ('2025-08-18', '08:30', '1', 'Tilapia', 1200, 0.6, 'Piscícola El Dorado', 'Ampliación población', 'Estanque comercial', 1200, 'Hembras 70%'),
            ('2025-08-19', '09:15', '2', 'Cachama', 900, 0.9, 'Acuicultura Moderna', 'Refuerzo poblacional', 'Estanque producción', 900, 'Machos 65%'),
            ('2025-08-20', '07:45', '3', 'Trucha', 750, 1.1, 'Truchas Premium', 'Línea genética mejorada', 'Estanque selectivo', 750, 'Mixto equilibrado')
        ]
        
        cursor.executemany('''
            INSERT INTO siembra (fecha, hora, estanque, especie, cantidad, peso_promedio, proveedor, observaciones, destino, ovas_alevinos, hembras_machos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', siembras_completas)
        
        print(f"   ✅ Insertados {len(siembras_completas)} registros de siembra")
        
        # Confirmar cambios
        conn.commit()
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ ACTUALIZACIÓN COMPLETA FINALIZADA")
        print("=" * 70)
        print("📊 RESUMEN:")
        print(f"   • Alimento: {len(alimentos_completos)} registros con mortalidad completa")
        print(f"   • Muestreo: {len(muestreos_completos)} registros con especies y biomasa")
        print(f"   • Parámetros: {len(parametros_completos)} registros con valores químicos")
        print(f"   • Siembra: {len(siembras_completas)} registros con destinos y poblaciones")
        print("\n🔍 Todos los formularios ahora tienen datos completos para pruebas")
        
    except Exception as e:
        print(f"❌ Error actualizando formularios: {e}")

def verificar_actualizacion():
    """Verificar que la actualización fue exitosa"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'piscicola.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n" + "=" * 50)
        print("🔍 VERIFICACIÓN DE ACTUALIZACIÓN")
        print("=" * 50)
        
        tablas = ['alimento', 'muestreo', 'parametros', 'siembra']
        
        for tabla in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            
            # Verificar algunos campos específicos
            if tabla == 'alimento':
                cursor.execute("SELECT COUNT(*) FROM alimento WHERE mortalidad > 0")
                con_mortalidad = cursor.fetchone()[0]
                print(f"📋 {tabla.upper()}: {count} registros ({con_mortalidad} con mortalidad)")
                
            elif tabla == 'muestreo':
                cursor.execute("SELECT COUNT(*) FROM muestreo WHERE especie IS NOT NULL")
                con_especie = cursor.fetchone()[0]
                print(f"📋 {tabla.upper()}: {count} registros ({con_especie} con especie)")
                
            elif tabla == 'parametros':
                cursor.execute("SELECT COUNT(*) FROM parametros WHERE oxigeno_disuelto IS NOT NULL")
                con_oxigeno = cursor.fetchone()[0]
                print(f"📋 {tabla.upper()}: {count} registros ({con_oxigeno} con oxígeno disuelto)")
                
            elif tabla == 'siembra':
                cursor.execute("SELECT COUNT(*) FROM siembra WHERE destino IS NOT NULL")
                con_destino = cursor.fetchone()[0]
                print(f"📋 {tabla.upper()}: {count} registros ({con_destino} con destino)")
        
        conn.close()
        print("\n✅ Verificación completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error verificando: {e}")

if __name__ == "__main__":
    actualizar_todos_formularios()
    verificar_actualizacion()
