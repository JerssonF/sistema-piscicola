# 🐟 Piscícola Fish River - Deployment Guide

Sistema de gestión para piscícola desarrollado en Flask.

## 🚀 Despliegue en Render.com

### Requisitos
- Cuenta en [Render.com](https://render.com)
- Repositorio en GitHub con el código

### Pasos para desplegar:

1. **Subir código a GitHub**:
   ```bash
   git add .
   git commit -m "Preparado para despliegue en Render"
   git push origin main
   ```

2. **Conectar con Render**:
   - Ve a [render.com](https://render.com)
   - Crea una cuenta o inicia sesión
   - Conecta tu cuenta de GitHub
   - Selecciona el repositorio `sistema-piscicola`

3. **Configurar el servicio**:
   - Tipo: Web Service
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment: Python 3

4. **Variables de entorno**:
   - `SECRET_KEY`: (se genera automáticamente)
   - `FLASK_ENV`: production

### 🌐 Características del despliegue:

- ✅ **Base de datos SQLite incluida**
- ✅ **Interfaz web responsiva**
- ✅ **Sistema de autenticación**
- ✅ **Gestión completa de piscícola**
- ✅ **HTTPS automático**
- ✅ **Dominio gratuito**

### 📋 Credenciales por defecto:
- **Usuario**: admin
- **Contraseña**: admin123

## 📁 Estructura del proyecto:
```
piscicola/
├── app.py              # Aplicación principal
├── config.py           # Configuración
├── requirements.txt    # Dependencias
├── Procfile           # Configuración Render
├── runtime.txt        # Versión Python
├── routes/            # Rutas de la aplicación
├── templates/         # Plantillas HTML
├── static/           # Archivos estáticos
└── models/           # Modelos de base de datos
```

## 🔧 Comandos útiles:

```bash
# Instalar dependencias localmente
pip install -r requirements.txt

# Ejecutar localmente
python app.py

# Inicializar base de datos
python init_db.py
```
