# 🔄 RECARGAR NAVEGADOR Y VERIFICAR ORDEN

Write-Host "🔄 VERIFICANDO ORDEN DE FECHAS" -ForegroundColor Green
Write-Host "================================`n" -ForegroundColor Green

# Verificar que el servidor esté corriendo
$pythonProcess = Get-Process -Name "python" -ErrorAction SilentlyContinue
if ($pythonProcess) {
    Write-Host "✅ Servidor Python está corriendo" -ForegroundColor Green
} else {
    Write-Host "❌ Servidor Python NO está corriendo" -ForegroundColor Red
    Write-Host "   Ejecuta: python app.py" -ForegroundColor Yellow
    exit
}

Write-Host "📋 Instrucciones para verificar el orden:" -ForegroundColor Cyan
Write-Host "  1. Abre el navegador en: http://localhost:5000" -ForegroundColor White
Write-Host "  2. Login: admin / admin123" -ForegroundColor White
Write-Host "  3. Ve a 'Formulario de Informes'" -ForegroundColor White
Write-Host "  4. Selecciona 'alimento' como formulario" -ForegroundColor White
Write-Host "  5. Pon fechas: desde 2025-08-01 hasta 2025-08-31" -ForegroundColor White
Write-Host "  6. Haz clic en 'Buscar'" -ForegroundColor White

Write-Host "`n📊 Orden esperado (de MENOR a MAYOR):" -ForegroundColor Cyan
Write-Host "  - 07/08/2025 (más antigua)" -ForegroundColor Yellow
Write-Host "  - 14/08/2025" -ForegroundColor Yellow
Write-Host "  - 21/08/2025" -ForegroundColor Yellow
Write-Host "  - 24/08/2025" -ForegroundColor Yellow
Write-Host "  - 25/08/2025" -ForegroundColor Yellow
Write-Host "  - 26/08/2025" -ForegroundColor Yellow
Write-Host "  - 30/08/2025 (más reciente)" -ForegroundColor Yellow

Write-Host "`n✅ CAMBIOS APLICADOS EN EL CÓDIGO:" -ForegroundColor Green
Write-Host "  ✅ ORDER BY fecha ASC (ascendente)" -ForegroundColor Green
Write-Host "  ✅ reverse=False (menor a mayor)" -ForegroundColor Green
Write-Host "  ✅ Indicador visual agregado" -ForegroundColor Green

Write-Host "`n🎯 Si las fechas aparecen en orden contrario al mostrado arriba," -ForegroundColor Cyan
Write-Host "   significa que los cambios aún no se han aplicado." -ForegroundColor Cyan

Write-Host "`nPresiona Enter para abrir el navegador..." -ForegroundColor Yellow
Read-Host

# Abrir navegador
Start-Process "http://localhost:5000/formulario_informes"
