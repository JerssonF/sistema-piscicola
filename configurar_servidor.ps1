# 🌐 CONFIGURACIÓN DEL SERVIDOR PISCÍCOLA

# Variables de entorno para el servidor
$env:FLASK_HOST = "0.0.0.0"      # Permite conexiones desde cualquier IP de la red
$env:FLASK_PORT = "5000"         # Puerto del servidor (cambiar si es necesario)
$env:FLASK_DEBUG = "False"       # Desactivar debug en producción

# Configuración de MySQL para red
$env:MYSQL_HOST = "localhost"    # O la IP del servidor MySQL
$env:MYSQL_PORT = "3306"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = ""
$env:MYSQL_DATABASE = "piscicola"

Write-Host "🌐 CONFIGURACIÓN DEL SERVIDOR PISCÍCOLA" -ForegroundColor Green
Write-Host "=====================================`n" -ForegroundColor Green

Write-Host "📋 Variables configuradas:" -ForegroundColor Cyan
Write-Host "  - FLASK_HOST: $env:FLASK_HOST" -ForegroundColor Yellow
Write-Host "  - FLASK_PORT: $env:FLASK_PORT" -ForegroundColor Yellow
Write-Host "  - MYSQL_HOST: $env:MYSQL_HOST" -ForegroundColor Yellow
Write-Host "  - MYSQL_PORT: $env:MYSQL_PORT" -ForegroundColor Yellow

Write-Host "`n🚀 Para iniciar el servidor ejecuta:" -ForegroundColor Cyan
Write-Host "     python app.py" -ForegroundColor White

Write-Host "`n🌍 El servidor estará disponible en:" -ForegroundColor Cyan
Write-Host "  - Local: http://localhost:$env:FLASK_PORT" -ForegroundColor White
Write-Host "  - Red:   http://[IP-de-este-PC]:$env:FLASK_PORT" -ForegroundColor White

Write-Host "`n📊 Para ver la IP de este PC:" -ForegroundColor Cyan
Write-Host "     ipconfig" -ForegroundColor White
