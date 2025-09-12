#!/usr/bin/env python3
"""
Script para identificar exactamente por qué el formulario no guarda
"""

def analizar_problemas_formulario():
    """Analizar los problemas específicos del formulario"""
    
    print("🔍 ANÁLISIS DE PROBLEMAS DEL FORMULARIO DE ALIMENTOS")
    print("=" * 60)
    
    print("\n1. CAMPOS EN EL TEMPLATE HTML:")
    campos_template = [
        'fecha',
        'frecuencia_toma',
        'estanque_celda', 
        'referencia_alimento',
        'cantidad_alimento',
        'mortalidad',
        'causa_mortalidad',
        'acciones_correctivas'
    ]
    
    for campo in campos_template:
        print(f"   ✅ {campo}")
    
    print("\n2. CAMPOS QUE ESPERA LA FUNCIÓN Flask:")
    campos_flask = [
        'fecha',
        'hora',  # ❌ FALTA EN TEMPLATE
        'estanque_celda',
        'referencia_alimento (se mapea a tipo_alimento)',
        'cantidad_alimento (se mapea a cantidad)',
        'observaciones'  # ❌ FALTA EN TEMPLATE
    ]
    
    for campo in campos_flask:
        if 'FALTA' in campo:
            print(f"   ❌ {campo}")
        else:
            print(f"   ✅ {campo}")
    
    print("\n3. CAMPOS ADICIONALES EN TEMPLATE (no procesados por Flask):")
    campos_extra = [
        'frecuencia_toma',
        'mortalidad', 
        'causa_mortalidad',
        'acciones_correctivas'
    ]
    
    for campo in campos_extra:
        print(f"   ⚠️  {campo} - No se procesa en app.py")
    
    print("\n4. SOLUCIONES NECESARIAS:")
    print("   🔧 Agregar campo 'hora' al template HTML")
    print("   🔧 Agregar campo 'observaciones' al template HTML")
    print("   🔧 Modificar app.py para procesar todos los campos del template")
    print("   🔧 O modificar el template para que coincida con app.py")

def generar_solucion():
    """Generar código de solución"""
    
    print("\n" + "=" * 60)
    print("💡 CÓDIGO DE SOLUCIÓN RECOMENDADO")
    print("=" * 60)
    
    print("""
OPCIÓN 1: Modificar app.py para procesar TODOS los campos del template:

```python
@app.route('/formulario_alimentos', methods=['GET', 'POST'])
def formulario_alimentos():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        try:
            # Campos básicos
            fecha = request.form['fecha']
            hora = request.form.get('hora', datetime.now().strftime('%H:%M'))  # Si no hay hora, usar actual
            estanque = request.form['estanque_celda']
            tipo_alimento = request.form['referencia_alimento']
            cantidad = float(request.form['cantidad_alimento'])
            
            # Campos adicionales del template
            frecuencia_toma = request.form.get('frecuencia_toma', '')
            mortalidad = int(request.form.get('mortalidad', 0))
            causa_mortalidad = request.form.get('causa_mortalidad', '')
            acciones_correctivas = request.form.get('acciones_correctivas', '')
            
            # Crear observaciones combinando los campos adicionales
            observaciones = f"Frecuencia: {frecuencia_toma}; Mortalidad: {mortalidad}; Causa: {causa_mortalidad}; Acciones: {acciones_correctivas}"
            
        except (ValueError, KeyError) as e:
            flash(f"Error en los datos del formulario: {e}", "error")
            return render_template('formulario_alimentos.html')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO alimento (fecha, hora, estanque, tipo_alimento, cantidad_kg, observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (fecha, hora, estanque, tipo_alimento, cantidad, observaciones, frecuencia_toma, mortalidad, causa_mortalidad, acciones_correctivas))
                
                conn.commit()
                flash("Alimento guardado correctamente.", "success")
                
            except Exception as e:
                flash(f"Error al guardar en la base de datos: {e}", "error")
            finally:
                conn.close()
        else:
            flash("Error de conexión a la base de datos.", "error")
        
        return redirect(url_for('formulario_alimentos'))

    return render_template('formulario_alimentos.html')
```

OPCIÓN 2: Agregar campo 'hora' al template HTML:

Agregar después del campo fecha:
```html
<div class="form-group">
    <label for="hora"><i class="fas fa-clock"></i> Hora:</label>
    <input type="time" id="hora" name="hora" required>
</div>
```
""")

def main():
    """Función principal"""
    analizar_problemas_formulario()
    generar_solucion()

if __name__ == "__main__":
    main()
