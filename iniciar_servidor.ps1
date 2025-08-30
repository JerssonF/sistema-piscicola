#!/usr/bin/env powershell
# 🚀 INICIO DEL SERVIDOR PISCÍCOLA EN RED LOCAL

Write-Host "🚀 INICIANDO SERVIDOR PISCÍCOLA" -ForegroundColor Green
Write-Host "================================`n" -ForegroundColor Green

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "app.py")) {
    Write-Host "❌ Error: No se encontró app.py" -ForegroundColor Red
    Write-Host "   Asegúrate de estar en el directorio del proyecto" -ForegroundColor Yellow
    pause
    exit 1
}

# Configurar variables de entorno para el servidor
$env:FLASK_HOST = "0.0.0.0"
$env:FLASK_PORT = "5000"
$env:FLASK_DEBUG = "False"

Write-Host "📋 Configuración del servidor:" -ForegroundColor Cyan
Write-Host "  - Host: $env:FLASK_HOST (permite conexiones remotas)" -ForegroundColor White
Write-Host "  - Puerto: $env:FLASK_PORT" -ForegroundColor White
Write-Host "  - Debug: $env:FLASK_DEBUG" -ForegroundColor White

# Verificar Python
Write-Host "`n🐍 Verificando Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no encontrado. Instala Python primero." -ForegroundColor Red
    pause
    exit 1
}

# Verificar dependencias
Write-Host "`n📦 Verificando dependencias..." -ForegroundColor Cyan
$requiredPackages = @("flask", "mysql-connector-python")
foreach ($package in $requiredPackages) {
    try {
        $result = pip show $package 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $package instalado" -ForegroundColor Green
        } else {
            Write-Host "❌ $package NO instalado" -ForegroundColor Red
            Write-Host "   Instalando $package..." -ForegroundColor Yellow
            pip install $package
        }
    } catch {
        Write-Host "⚠️  No se pudo verificar $package" -ForegroundColor Yellow
    }
}

# Verificar XAMPP/MySQL
Write-Host "`n🗄️ Verificando MySQL..." -ForegroundColor Cyan
$mysqlProcess = Get-Process -Name "mysqld" -ErrorAction SilentlyContinue
if ($mysqlProcess) {
    Write-Host "✅ MySQL está corriendo" -ForegroundColor Green
} else {
    Write-Host "❌ MySQL no está corriendo" -ForegroundColor Red
    Write-Host "   ⚠️  Inicia XAMPP Control Panel y activa MySQL" -ForegroundColor Yellow
    $response = Read-Host "¿Quieres que abra XAMPP Control Panel? (s/N)"
    if ($response -eq "s" -or $response -eq "S") {
        try {
            Start-Process "C:\xampp\xampp-control.exe" -Verb RunAs
            Write-Host "📋 Esperando que inicies MySQL en XAMPP..." -ForegroundColor Yellow
            Read-Host "Presiona Enter cuando MySQL esté corriendo"
        } catch {
            Write-Host "❌ No se pudo abrir XAMPP. Ábrelo manualmente." -ForegroundColor Red
            pause
        }
    }
}

# Probar conexión a base de datos
Write-Host "`n🔍 Probando conexión a base de datos..." -ForegroundColor Cyan
try {
    $result = python database_config.py 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Conexión a base de datos exitosa" -ForegroundColor Green
    } else {
        Write-Host "❌ Error en conexión a base de datos" -ForegroundColor Red
        Write-Host $result -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  No se pudo probar la conexión" -ForegroundColor Yellow
}

# Obtener IP del servidor
Write-Host "`n🌐 Información de red:" -ForegroundColor Cyan
try {
    $ipInfo = Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*", "Ethernet*" | Where-Object { $_.IPAddress -notmatch "^127\." }
    if ($ipInfo) {
        $serverIP = $ipInfo[0].IPAddress
        Write-Host "  📍 IP del servidor: $serverIP" -ForegroundColor Green
        Write-Host "  🔗 URL local: http://localhost:$env:FLASK_PORT" -ForegroundColor White
        Write-Host "  🌍 URL remota: http://$serverIP`:$env:FLASK_PORT" -ForegroundColor Yellow
    } else {
        Write-Host "  ⚠️  No se pudo obtener IP del servidor" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ Error obteniendo información de red" -ForegroundColor Red
}

# Información para otros PCs
Write-Host "`n👥 Para conectar otros PCs:" -ForegroundColor Cyan
Write-Host "  1. Asegúrate que están en la misma red" -ForegroundColor White
Write-Host "  2. Usa la URL: http://$serverIP`:$env:FLASK_PORT" -ForegroundColor White
Write-Host "  3. Credenciales: admin / admin123" -ForegroundColor White

# Configuración de Firewall
Write-Host "`n🔥 Configuración de Firewall:" -ForegroundColor Cyan
Write-Host "  ⚠️  Si otros PCs no pueden conectar, revisa:" -ForegroundColor Yellow
Write-Host "     - Windows Firewall (puerto $env:FLASK_PORT)" -ForegroundColor White
Write-Host "     - Antivirus" -ForegroundColor White
Write-Host "     - Configuración del router" -ForegroundColor White

Write-Host "`n🚀 INICIANDO SERVIDOR..." -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host "📋 Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host "🌐 El servidor estará disponible en las URLs mostradas arriba`n" -ForegroundColor Cyan

# Iniciar el servidor Flask
try {
    python app.py
} catch {
    Write-Host "`n❌ Error al iniciar el servidor" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
}

Write-Host "`n🛑 Servidor detenido" -ForegroundColor Yellow
pause
