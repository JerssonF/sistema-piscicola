# 🌐 CONFIGURACIÓN DEL SERVIDOR PISCÍCOLA PARA RED LOCAL

## 📋 PASOS PARA CONFIGURAR EL SERVIDOR

### 1. 🖥️ **Preparación del PC Servidor (donde está la base de datos)**

#### **Paso 1.1: Configurar XAMPP para Red**
```bash
1. Abrir XAMPP Control Panel como Administrador
2. Iniciar Apache y MySQL
3. Clic en "Config" de MySQL → "my.ini"
4. Buscar la línea: bind-address = 127.0.0.1
5. Cambiar por: bind-address = 0.0.0.0
6. Guardar y reiniciar MySQL en XAMPP
```

#### **Paso 1.2: Configurar MySQL para Acceso Remoto**
```powershell
# Ejecutar este script:
.\configurar_mysql_red.ps1
```

#### **Paso 1.3: Configurar Firewall de Windows**
```bash
1. Abrir "Windows Firewall con seguridad avanzada"
2. Crear nueva regla de entrada:
   - Tipo: Puerto
   - Protocolo: TCP
   - Puerto: 5000 (Flask)
3. Crear otra regla para puerto 3306 (MySQL)
4. Permitir conexiones para ambas reglas
```

### 2. 🚀 **Iniciar el Servidor**

#### **Opción A: Script Automático (Recomendado)**
```powershell
# Ejecutar desde PowerShell como Administrador:
.\iniciar_servidor.ps1
```

#### **Opción B: Manual**
```powershell
# 1. Configurar variables de entorno:
.\configurar_servidor.ps1

# 2. Iniciar servidor:
python app.py
```

### 3. 💻 **Configuración de PCs Clientes**

#### **Paso 3.1: Obtener IP del Servidor**
```powershell
# En el PC servidor, ejecutar:
ipconfig
# Anotar la IP (ejemplo: 192.168.1.100)
```

#### **Paso 3.2: Acceso desde PCs Clientes**
```bash
URL de acceso: http://[IP-DEL-SERVIDOR]:5000
Ejemplo: http://192.168.1.100:5000

Credenciales:
Usuario: admin
Contraseña: admin123
```

---

## 🔧 CONFIGURACIÓN TÉCNICA DETALLADA

### **Puertos Utilizados:**
- **5000**: Servidor Flask (aplicación web)
- **3306**: MySQL (base de datos)
- **80**: Apache (opcional, para phpMyAdmin)

### **Credenciales de Base de Datos:**
- **Local**: 
  - Usuario: `root`
  - Contraseña: (vacía)
- **Remoto**: 
  - Usuario: `piscicola_user`
  - Contraseña: `piscicola123`

### **Variables de Entorno:**
```bash
FLASK_HOST=0.0.0.0          # Permite conexiones desde cualquier IP
FLASK_PORT=5000             # Puerto del servidor web
MYSQL_HOST=localhost        # IP del servidor MySQL
MYSQL_PORT=3306             # Puerto de MySQL
MYSQL_USER=root             # Usuario de MySQL
MYSQL_DATABASE=piscicola    # Nombre de la base de datos
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### **❌ Error: "No se puede conectar al servidor"**
```bash
Soluciones:
1. Verificar que el servidor esté corriendo
2. Verificar IP y puerto correctos
3. Revisar Firewall de Windows
4. Verificar que ambos PCs estén en la misma red
5. Probar con ping: ping [IP-DEL-SERVIDOR]
```

### **❌ Error: "Error de base de datos"**
```bash
Soluciones:
1. Verificar que MySQL esté corriendo
2. Probar conexión local primero
3. Ejecutar: .\configurar_mysql_red.ps1
4. Verificar credenciales de base de datos
5. Revisar logs de MySQL en XAMPP
```

### **❌ Error: "Puerto 5000 en uso"**
```bash
Soluciones:
1. Cambiar puerto en configurar_servidor.ps1
2. Matar procesos: taskkill /F /IM python.exe
3. Reiniciar el PC si es necesario
```

### **❌ Error: "Acceso denegado desde otro PC"**
```bash
Soluciones:
1. Verificar configuración de Firewall
2. Revisar configuración de MySQL (bind-address)
3. Verificar permisos de usuario MySQL
4. Probar conexión local primero
```

---

## 📊 VERIFICACIÓN DEL SISTEMA

### **Test de Conexión Local:**
```powershell
# Probar aplicación local:
curl http://localhost:5000

# Probar base de datos:
python database_config.py
```

### **Test de Conexión Remota:**
```powershell
# Desde otro PC:
ping [IP-DEL-SERVIDOR]
curl http://[IP-DEL-SERVIDOR]:5000

# Probar conexión a MySQL:
telnet [IP-DEL-SERVIDOR] 3306
```

---

## 🌟 CARACTERÍSTICAS DEL SERVIDOR

- ✅ **Soporte Multi-Cliente**: Múltiples PCs pueden conectar simultáneamente
- ✅ **Failover Automático**: Conexión local/remota automática
- ✅ **Base de Datos Centralizada**: Un solo repositorio de datos
- ✅ **Interfaz Glass Premium**: Mantenida en todos los clientes
- ✅ **Sesiones Independientes**: Cada PC mantiene su sesión
- ✅ **Backup Automático**: Todos los datos en un solo lugar

---

## 🎯 ARQUITECTURA DEL SISTEMA

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PC Cliente 1  │    │   PC Cliente 2  │    │   PC Cliente N  │
│                 │    │                 │    │                 │
│  Navegador Web  │    │  Navegador Web  │    │  Navegador Web  │
│                 │    │                 │    │                 │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │         HTTP :5000   │        HTTP :5000    │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      PC SERVIDOR        │
                    │                         │
                    │  ┌─────────────────┐   │
                    │  │  Flask Server   │   │
                    │  │   (Puerto 5000) │   │
                    │  └─────────┬───────┘   │
                    │            │           │
                    │  ┌─────────▼───────┐   │
                    │  │  MySQL Server   │   │
                    │  │   (Puerto 3306) │   │
                    │  │                 │   │
                    │  │  BD: piscicola  │   │
                    │  └─────────────────┘   │
                    └─────────────────────────┘
```

---

## 📞 SOPORTE

Si tienes problemas:
1. Ejecuta `python database_config.py` para diagnóstico
2. Revisa los logs del servidor
3. Verifica la configuración de red
4. Consulta la sección de solución de problemas

**¡El sistema está listo para trabajar en red local!** 🎉
