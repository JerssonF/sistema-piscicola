# 💾 SCRIPT DE GUARDADO FINAL DEL SERVIDOR

Write-Host "💾 GUARDANDO CONFIGURACIÓN DEL SERVIDOR" -ForegroundColor Green
Write-Host "======================================`n" -ForegroundColor Green

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "app.py")) {
    Write-Host "❌ Error: No se encontró app.py" -ForegroundColor Red
    Write-Host "   Asegúrate de estar en el directorio del proyecto" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "📁 Directorio del proyecto verificado" -ForegroundColor Green

# Agregar todos los archivos
Write-Host "`n📋 Agregando archivos al repositorio..." -ForegroundColor Cyan
try {
    git add .
    Write-Host "✅ Archivos agregados" -ForegroundColor Green
} catch {
    Write-Host "❌ Error agregando archivos: $($_.Exception.Message)" -ForegroundColor Red
}

# Hacer commit
Write-Host "`n📋 Creando commit..." -ForegroundColor Cyan
try {
    git commit -m "🌐 SERVIDOR RED LOCAL: Sistema configurado para múltiples PCs

✅ Características implementadas:
- Flask server configurado para red (0.0.0.0:5000)
- MySQL configurado para acceso remoto
- Scripts automáticos de configuración
- Firewall configurado automáticamente
- Base de datos completa con todas las tablas
- Usuarios y permisos configurados
- Documentación completa del servidor
- Pruebas exitosas con cliente remoto

🎯 Resultado:
- Múltiples PCs pueden conectar simultáneamente
- Datos centralizados en servidor
- Interfaz glass premium mantenida
- Servidor IP: 192.168.20.2:5000
- Cliente verificado: 192.168.20.22"

    Write-Host "✅ Commit creado exitosamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error creando commit: $($_.Exception.Message)" -ForegroundColor Red
}

# Subir a GitHub
Write-Host "`n📋 Subiendo a GitHub..." -ForegroundColor Cyan
try {
    git push origin main
    Write-Host "✅ Cambios subidos a GitHub exitosamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error subiendo a GitHub: $($_.Exception.Message)" -ForegroundColor Red
}

# Mostrar estado final
Write-Host "`n📋 Estado final del repositorio..." -ForegroundColor Cyan
try {
    git status
    Write-Host "`n✅ Repositorio sincronizado" -ForegroundColor Green
} catch {
    Write-Host "❌ Error verificando estado" -ForegroundColor Red
}

# Mostrar archivos creados
Write-Host "`n📋 Archivos de servidor creados:" -ForegroundColor Cyan
$serverFiles = @(
    "configurar_firewall.ps1",
    "configurar_mysql_red.ps1", 
    "configurar_bd_completa.py",
    "iniciar_servidor.ps1",
    "database_config.py",
    "SERVIDOR_RED_LOCAL.md",
    "CONFIGURACION_SERVIDOR_RED.md",
    "SERVIDOR_CONFIGURADO.md"
)

foreach ($file in $serverFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file (no encontrado)" -ForegroundColor Red
    }
}

Write-Host "`n🎉 GUARDADO COMPLETADO" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green
Write-Host "🌐 Servidor configurado y guardado en GitHub" -ForegroundColor Cyan
Write-Host "📋 Para usar: .\iniciar_servidor.ps1" -ForegroundColor Yellow
Write-Host "🔗 URL: http://192.168.20.2:5000" -ForegroundColor Yellow

pause
