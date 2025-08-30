# 🌐 SERVIDOR PISCÍCOLA - CONFIGURACIÓN DE RED LOCAL

## 🚀 INICIO RÁPIDO

### **Para el PC Servidor (donde está la base de datos):**

1. **📥 Configurar Firewall (Como Administrador)**
   ```powershell
   .\configurar_firewall.ps1
   ```

2. **🗄️ Configurar Base de Datos**
   ```powershell
   python configurar_bd_completa.py
   ```

3. **🚀 Iniciar Servidor**
   ```powershell
   .\iniciar_servidor.ps1
   ```

### **Para PCs Clientes:**
1. Obtener IP del servidor (mostrada al iniciar)
2. Abrir navegador en: `http://[IP-SERVIDOR]:5000`
3. Login: `admin` / `admin123`

---

## 📋 ARQUITECTURA DEL SISTEMA

```
🖥️ PC Cliente 1 ────┐
                    │
🖥️ PC Cliente 2 ────┼─── HTTP:5000 ──→ 🖥️ PC SERVIDOR
                    │                    │
🖥️ PC Cliente N ────┘                    ├─ Flask App (Puerto 5000)
                                         └─ MySQL DB (Puerto 3306)
```

## ✅ CARACTERÍSTICAS

- 🌐 **Multi-Cliente**: Varios PCs simultáneos
- 🔄 **Datos Centralizados**: Una sola base de datos
- 💾 **Auto-Backup**: Todos los datos en el servidor
- 🎨 **Interfaz Glass**: Mantenida en todos los clientes
- 🔒 **Sesiones Independientes**: Cada PC su sesión
- 📊 **Informes Centralizados**: Datos de todos los PCs

## 🔧 CONFIGURACIÓN TÉCNICA

### **Puertos:**
- `5000`: Aplicación Web Flask
- `3306`: Base de Datos MySQL

### **Credenciales:**
- **App**: `admin` / `admin123`
- **DB Local**: `root` / (sin contraseña)
- **DB Remoto**: `piscicola_user` / `piscicola123`

### **URLs de Acceso:**
- **Local**: `http://localhost:5000`
- **Red**: `http://[IP-SERVIDOR]:5000`

## 🛠️ SCRIPTS DISPONIBLES

| Script | Descripción |
|--------|-------------|
| `configurar_firewall.ps1` | Configura Windows Firewall automáticamente |
| `configurar_bd_completa.py` | Configura base de datos completa |
| `iniciar_servidor.ps1` | Inicia el servidor con verificaciones |
| `database_config.py` | Prueba conexiones de base de datos |

## 🚨 SOLUCIÓN DE PROBLEMAS

### **❌ No se puede conectar desde otro PC**
```bash
Soluciones:
1. Verificar Firewall: .\configurar_firewall.ps1
2. Verificar IP: ipconfig
3. Probar ping: ping [IP-SERVIDOR]
4. Verificar que están en la misma red
```

### **❌ Error de base de datos**
```bash
Soluciones:
1. Verificar XAMPP activo (MySQL)
2. Ejecutar: python configurar_bd_completa.py
3. Verificar conexión: python database_config.py
```

### **❌ Puerto en uso**
```bash
Soluciones:
1. Matar procesos: taskkill /F /IM python.exe
2. Cambiar puerto en configurar_servidor.ps1
3. Reiniciar PC si es necesario
```

## 📊 MONITOREO

### **Verificar Estado del Servidor:**
```powershell
# Procesos activos
Get-Process | Where-Object {$_.ProcessName -eq "python"}

# Puertos en uso
netstat -an | findstr ":5000"
netstat -an | findstr ":3306"

# Test de conexión
python database_config.py
```

### **Ver Logs:**
- Los logs aparecen en la consola donde se ejecuta `iniciar_servidor.ps1`
- Errores de MySQL en XAMPP Control Panel

## 🎯 VENTAJAS DEL SERVIDOR

- ✅ **Centralización**: Todos los datos en un lugar
- ✅ **Colaboración**: Múltiples usuarios simultáneos
- ✅ **Backup Automático**: Datos seguros en el servidor
- ✅ **Actualizaciones**: Solo actualizar el servidor
- ✅ **Rendimiento**: Base de datos optimizada
- ✅ **Seguridad**: Control centralizado de acceso

## 🌟 ESTADO ACTUAL

- ✅ **Servidor Flask**: Configurado para red (0.0.0.0:5000)
- ✅ **Base de Datos**: MySQL configurado para acceso remoto
- ✅ **Firewall**: Scripts automáticos disponibles
- ✅ **Usuarios**: Admin creado, acceso remoto configurado
- ✅ **Tablas**: Todas las tablas verificadas y funcionales
- ✅ **Interfaz**: Efectos glass mantenidos
- ✅ **Scripts**: Automatización completa disponible

---

## 🎉 **¡SERVIDOR LISTO PARA PRODUCCIÓN!**

**El sistema ahora puede manejar múltiples PCs conectados simultáneamente con datos centralizados y interfaz premium.**
