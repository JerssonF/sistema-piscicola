# 🔥 CONFIGURACIÓN AUTOMÁTICA DEL FIREWALL

Write-Host "🔥 CONFIGURANDO FIREWALL PARA SERVIDOR PISCÍCOLA" -ForegroundColor Green
Write-Host "================================================`n" -ForegroundColor Green

# Verificar si se ejecuta como administrador
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Este script debe ejecutarse como Administrador" -ForegroundColor Red
    Write-Host "   Haz clic derecho y selecciona 'Ejecutar como administrador'" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✅ Ejecutándose como Administrador" -ForegroundColor Green

# Configurar reglas de Firewall
try {
    Write-Host "`n📋 Configurando reglas de Firewall..." -ForegroundColor Cyan
    
    # Regla para Flask (puerto 5000)
    Write-Host "  🌐 Configurando puerto 5000 (Flask)..." -ForegroundColor White
    try {
        # Eliminar regla existente si existe
        Remove-NetFirewallRule -DisplayName "Sistema Piscicola - Flask" -ErrorAction SilentlyContinue
        
        # Crear nueva regla
        New-NetFirewallRule -DisplayName "Sistema Piscicola - Flask" `
                           -Direction Inbound `
                           -Protocol TCP `
                           -LocalPort 5000 `
                           -Action Allow `
                           -Profile Any `
                           -Description "Permite acceso al servidor Flask del Sistema Piscícola"
        
        Write-Host "    ✅ Regla para puerto 5000 creada" -ForegroundColor Green
    } catch {
        Write-Host "    ❌ Error configurando puerto 5000: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Regla para MySQL (puerto 3306)
    Write-Host "  🗄️ Configurando puerto 3306 (MySQL)..." -ForegroundColor White
    try {
        # Eliminar regla existente si existe
        Remove-NetFirewallRule -DisplayName "Sistema Piscicola - MySQL" -ErrorAction SilentlyContinue
        
        # Crear nueva regla
        New-NetFirewallRule -DisplayName "Sistema Piscicola - MySQL" `
                           -Direction Inbound `
                           -Protocol TCP `
                           -LocalPort 3306 `
                           -Action Allow `
                           -Profile Any `
                           -Description "Permite acceso al servidor MySQL del Sistema Piscícola"
        
        Write-Host "    ✅ Regla para puerto 3306 creada" -ForegroundColor Green
    } catch {
        Write-Host "    ❌ Error configurando puerto 3306: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host "`n✅ Configuración de Firewall completada" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error general configurando Firewall: $($_.Exception.Message)" -ForegroundColor Red
}

# Verificar reglas creadas
Write-Host "`n📋 Verificando reglas creadas..." -ForegroundColor Cyan
try {
    $flaskRule = Get-NetFirewallRule -DisplayName "Sistema Piscicola - Flask" -ErrorAction SilentlyContinue
    $mysqlRule = Get-NetFirewallRule -DisplayName "Sistema Piscicola - MySQL" -ErrorAction SilentlyContinue
    
    if ($flaskRule) {
        Write-Host "  ✅ Regla Flask (5000): Activa" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Regla Flask (5000): No encontrada" -ForegroundColor Red
    }
    
    if ($mysqlRule) {
        Write-Host "  ✅ Regla MySQL (3306): Activa" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Regla MySQL (3306): No encontrada" -ForegroundColor Red
    }
    
} catch {
    Write-Host "  ⚠️ No se pudieron verificar las reglas" -ForegroundColor Yellow
}

# Información adicional
Write-Host "`n📋 Información adicional:" -ForegroundColor Cyan
Write-Host "  • Las reglas permiten conexiones desde cualquier IP" -ForegroundColor White
Write-Host "  • Se aplicó a todos los perfiles (Dominio, Privado, Público)" -ForegroundColor White
Write-Host "  • Para ver todas las reglas: Windows Firewall > Reglas de entrada" -ForegroundColor White

# Mostrar IP del servidor
try {
    $ipInfo = Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*", "Ethernet*" | Where-Object { $_.IPAddress -notmatch "^127\." }
    if ($ipInfo) {
        $serverIP = $ipInfo[0].IPAddress
        Write-Host "`n🌐 IP de este servidor: $serverIP" -ForegroundColor Green
        Write-Host "  📱 Los otros PCs podrán acceder en: http://$serverIP`:5000" -ForegroundColor Yellow
    }
} catch {
    Write-Host "`n⚠️ No se pudo obtener la IP del servidor" -ForegroundColor Yellow
}

Write-Host "`n🎉 CONFIGURACIÓN DE FIREWALL COMPLETADA" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host "📋 Ahora puedes ejecutar: .\iniciar_servidor.ps1" -ForegroundColor Cyan

pause
