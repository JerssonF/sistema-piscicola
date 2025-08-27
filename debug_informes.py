#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from routes import get_db_connection

def test_informes_query():
    """Simular la consulta de informes para debug"""
    print("🔍 PROBANDO CONSULTA DE INFORMES...")
    
    conn = get_db_connection()
    if not conn:
        print("❌ Error de conexión a la base de datos")
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Simular filtros (sin filtros específicos)
        formulario = ""
        fecha_desde = "2025-08-01"
        fecha_hasta = "2025-08-26"
        estanque = ""
        
        print(f"📊 FILTROS DE PRUEBA:")
        print(f"   formulario='{formulario}'")
        print(f"   fecha_desde='{fecha_desde}'")
        print(f"   fecha_hasta='{fecha_hasta}'")
        print(f"   estanque='{estanque}'")
        
        resultados = []
        tablas_query = ['alimento', 'ingreso_alimentos', 'muestreo', 'parametros', 'siembra']
        
        for tabla in tablas_query:
            try:
                print(f"\n🔍 CONSULTANDO TABLA: {tabla}")
                
                query = f"SELECT *, '{tabla}' as tipo FROM {tabla} WHERE 1=1"
                params = []
                
                if fecha_desde:
                    query += " AND fecha >= %s"
                    params.append(fecha_desde)
                    
                if fecha_hasta:
                    query += " AND fecha <= %s"
                    params.append(fecha_hasta)
                
                query += " ORDER BY fecha DESC LIMIT 5"
                
                print(f"📋 SQL: {query}")
                print(f"📊 PARAMS: {params}")
                
                cursor.execute(query, params)
                registros = cursor.fetchall()
                
                print(f"✅ ENCONTRADOS: {len(registros)} registros")
                
                for i, registro in enumerate(registros):
                    print(f"   📄 Registro {i+1}:")
                    print(f"      ID: {registro.get('id')}")
                    print(f"      Fecha: {registro.get('fecha')}")
                    print(f"      Tipo: {registro.get('tipo')}")
                    print(f"      Estanque: {registro.get('estanque_celda', 'N/A')}")
                    
                    # Mostrar campos específicos según el tipo
                    if tabla == 'alimento':
                        print(f"      Referencia: {registro.get('referencia_alimento')}")
                        print(f"      Cantidad: {registro.get('cantidad_alimento')}")
                    elif tabla == 'muestreo':
                        print(f"      Especie: {registro.get('especie')}")
                        print(f"      Peces: {registro.get('peces')}")
                    
                resultados.extend(registros)
                
            except Exception as e:
                print(f"❌ ERROR en tabla {tabla}: {e}")
                continue
        
        print(f"\n🎯 TOTAL COMBINADO: {len(resultados)} registros")
        
        # Verificar que los registros tengan la estructura correcta
        if resultados:
            print(f"\n🔍 ESTRUCTURA DEL PRIMER REGISTRO:")
            primer_registro = resultados[0]
            for key, value in primer_registro.items():
                print(f"   {key}: {value} ({type(value).__name__})")
        
    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_informes_query()
