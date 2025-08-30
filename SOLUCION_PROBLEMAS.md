# 🔧 GUÍA DE SOLUCIÓN RÁPIDA - SISTEMA PISCÍCOLA

## ✅ VERIFICACIÓN RÁPIDA

### 🌐 **Estado del Servidor**
- **URL Principal:** http://192.168.20.2:5000
- **URL Local:** http://localhost:5000
- **Usuario:** admin
- **Contraseña:** admin123

### 🔍 **Si algo no funciona:**

#### 1. **Problema de Carga de Página**
```
✅ Solución:
- Presiona Ctrl+F5 (Windows) o Cmd+Shift+R (Mac) para limpiar caché
- En móvil: Refresca la página deslizando hacia abajo
```

#### 2. **Problema de Estilo/Diseño**
```
✅ Solución:
- Verifica que la URL sea exactamente: http://192.168.20.2:5000
- Si usas localhost, cambia a la IP: 192.168.20.2
- Limpia caché del navegador
```

#### 3. **Problema de Acceso desde otro PC**
```
✅ Solución:
- Verifica que ambos PCs estén en la misma red WiFi
- Usa la IP del servidor: 192.168.20.2:5000
- Verifica que Windows Firewall permita el puerto 5000
```

#### 4. **Problema en Móvil**
```
✅ Solución:
- Usa Chrome o Firefox en el móvil
- Asegúrate de estar en la misma WiFi
- URL: http://192.168.20.2:5000
- Si se ve pequeño, gira el teléfono a horizontal
```

## 🚀 **REINICIO COMPLETO**

### Opción 1: Comando Rápido
```bash
# En PowerShell:
Get-Process python | Stop-Process -Force
cd "c:\Users\USUARIO\Desktop\JERSSON\piscicola"
python app.py
```

### Opción 2: Archivo Batch
```
Ejecuta: reiniciar_servidor.bat
```

## 📱 **FUNCIONES PRINCIPALES**

### 🏠 **Dashboard**
- Resumen general del sistema
- Enlaces rápidos a todas las funciones

### 📊 **Informes** (Principal)
- Búsqueda por tipo de formulario
- Filtros por fecha y estanque
- Tablas con scroll horizontal en móvil

### 📝 **Formularios**
- **Alimentos:** Registro diario de alimentación
- **Ingreso de Alimentos:** Control de inventario
- **Muestreo:** Peso y talla de peces
- **Parámetros:** Calidad del agua
- **Siembra:** Control de población

## 🎯 **CARACTERÍSTICAS RESPONSIVE**

### 📱 **En Móvil:**
- Menú adaptativo
- Botones grandes para touch
- Tablas con scroll horizontal
- Formularios optimizados
- Indicador "Desliza para ver más"

### 💻 **En Desktop:**
- Vista completa de tablas
- Menú desplegable completo
- Formularios en múltiples columnas

## ⚠️ **PROBLEMAS COMUNES Y SOLUCIONES**

### 🔴 **Error: "No se puede conectar"**
```
Causa: Servidor no iniciado o IP incorrecta
Solución: 
1. Verificar que python app.py esté corriendo
2. Usar IP correcta: 192.168.20.2:5000
```

### 🔴 **Error: "Página en blanco"**
```
Causa: Caché del navegador
Solución:
1. Ctrl+F5 para limpiar caché
2. Probar en navegador privado/incógnito
```

### 🔴 **Error: "Diseño roto"**
```
Causa: CSS no carga correctamente
Solución:
1. Verificar URL exacta
2. Limpiar caché del navegador
3. Reiniciar servidor
```

### 🔴 **Error: "No funciona en móvil"**
```
Causa: Configuración de red o navegador
Solución:
1. Verificar WiFi (misma red)
2. Usar Chrome o Firefox
3. URL completa: http://192.168.20.2:5000
```

## 📞 **CONTACTO TÉCNICO**

Si ninguna solución funciona:
1. Reinicia el servidor con `python app.py`
2. Verifica la consola en busca de errores
3. Prueba desde otro dispositivo

---
**Sistema Piscícola v2.0 - Optimizado para Móviles**
*Jersson Fabian Buitrago - 2025*
