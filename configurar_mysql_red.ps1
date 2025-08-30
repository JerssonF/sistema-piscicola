# 🗄️ CONFIGURACIÓN DE MYSQL PARA RED LOCAL

Write-Host "🗄️ CONFIGURANDO MYSQL PARA RED LOCAL" -ForegroundColor Green
Write-Host "====================================`n" -ForegroundColor Green

# Paso 1: Verificar que MySQL está corriendo
Write-Host "📋 Paso 1: Verificando estado de MySQL..." -ForegroundColor Cyan
$mysqlProcess = Get-Process -Name "mysqld" -ErrorAction SilentlyContinue
if ($mysqlProcess) {
    Write-Host "✅ MySQL está corriendo" -ForegroundColor Green
} else {
    Write-Host "❌ MySQL no está corriendo. Inicia XAMPP primero." -ForegroundColor Red
    Write-Host "   Abre XAMPP Control Panel y inicia Apache y MySQL" -ForegroundColor Yellow
    pause
    exit
}

# Paso 2: Mostrar configuración actual
Write-Host "`n📋 Paso 2: Configuración actual de MySQL..." -ForegroundColor Cyan

# Verificar conexión local
try {
    $result = & "C:\xampp\mysql\bin\mysql.exe" -u root -e "SELECT 'Conexión exitosa' as status;" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Conexión local MySQL exitosa" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error de conexión local a MySQL" -ForegroundColor Red
}

# Paso 3: Configurar usuario para acceso remoto
Write-Host "`n📋 Paso 3: Configurando acceso remoto..." -ForegroundColor Cyan

$sqlCommands = @"
-- Crear usuario para acceso remoto (si no existe)
CREATE USER IF NOT EXISTS 'piscicola_user'@'%' IDENTIFIED BY 'piscicola123';

-- Otorgar permisos completos a la base de datos piscicola
GRANT ALL PRIVILEGES ON piscicola.* TO 'piscicola_user'@'%';
GRANT ALL PRIVILEGES ON piscicola.* TO 'root'@'%';

-- Refrescar privilegios
FLUSH PRIVILEGES;

-- Verificar usuarios creados
SELECT User, Host FROM mysql.user WHERE User IN ('root', 'piscicola_user');
"@

# Ejecutar comandos SQL
try {
    $sqlCommands | & "C:\xampp\mysql\bin\mysql.exe" -u root
    Write-Host "✅ Configuración de acceso remoto completada" -ForegroundColor Green
} catch {
    Write-Host "❌ Error al configurar acceso remoto" -ForegroundColor Red
}

# Paso 4: Verificar que la base de datos piscicola existe
Write-Host "`n📋 Paso 4: Verificando base de datos..." -ForegroundColor Cyan
try {
    $databases = & "C:\xampp\mysql\bin\mysql.exe" -u root -e "SHOW DATABASES LIKE 'piscicola';" 2>$null
    if ($databases -match "piscicola") {
        Write-Host "✅ Base de datos 'piscicola' encontrada" -ForegroundColor Green
        
        # Verificar tablas
        $tables = & "C:\xampp\mysql\bin\mysql.exe" -u root -e "USE piscicola; SHOW TABLES;" 2>$null
        $tableCount = ($tables -split "`n" | Where-Object { $_ -and $_ -notmatch "Tables_in_" }).Count
        Write-Host "📊 Tablas encontradas: $tableCount" -ForegroundColor Yellow
    } else {
        Write-Host "❌ Base de datos 'piscicola' no encontrada" -ForegroundColor Red
        Write-Host "   Necesitas crear la base de datos primero" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error al verificar base de datos" -ForegroundColor Red
}

# Paso 5: Obtener IP de este PC
Write-Host "`n📋 Paso 5: Información de red..." -ForegroundColor Cyan
$ipInfo = Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*", "Ethernet*" | Where-Object { $_.IPAddress -notmatch "^127\." }
if ($ipInfo) {
    $serverIP = $ipInfo[0].IPAddress
    Write-Host "🌐 IP del servidor: $serverIP" -ForegroundColor Green
    Write-Host "🔗 URL de acceso remoto: http://$serverIP:5000" -ForegroundColor Yellow
} else {
    Write-Host "❌ No se pudo obtener la IP del servidor" -ForegroundColor Red
}

# Paso 6: Configuración del Firewall (opcional)
Write-Host "`n📋 Paso 6: Configuración de Firewall..." -ForegroundColor Cyan
Write-Host "⚠️  Para permitir conexiones externas, asegúrate de:" -ForegroundColor Yellow
Write-Host "   1. Abrir puerto 5000 en Windows Firewall (Flask)" -ForegroundColor White
Write-Host "   2. Abrir puerto 3306 en Windows Firewall (MySQL)" -ForegroundColor White
Write-Host "   3. Configurar el router si es necesario" -ForegroundColor White

Write-Host "`n✅ CONFIGURACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "==========================`n" -ForegroundColor Green

Write-Host "📋 Credenciales de base de datos:" -ForegroundColor Cyan
Write-Host "  - Usuario local: root (sin contraseña)" -ForegroundColor White
Write-Host "  - Usuario remoto: piscicola_user" -ForegroundColor White
Write-Host "  - Contraseña remota: piscicola123" -ForegroundColor White
Write-Host "  - Base de datos: piscicola" -ForegroundColor White
Write-Host "  - Puerto: 3306" -ForegroundColor White

Write-Host "`n🚀 Siguiente paso: Ejecutar 'python app.py' para iniciar el servidor" -ForegroundColor Green
