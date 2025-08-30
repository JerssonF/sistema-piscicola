@echo off
echo 🔄 REINICIANDO SISTEMA PISCICOLA...
echo.

echo 🛑 Deteniendo procesos Python...
taskkill /f /im python.exe >nul 2>&1

echo 🧹 Limpiando caché...
timeout /t 2 >nul

echo 🚀 Iniciando servidor...
cd /d "c:\Users\USUARIO\Desktop\JERSSON\piscicola"
python app.py

pause
