# 🐟 Sistema de Gestión Piscícola

Un sistema web desarrollado en Flask para la gestión integral de granjas piscícolas con interfaz profesional y efectos glass modernos.

![Flask](https://img.shields.io/badge/Flask-2.3.0-blue) ![MySQL](https://img.shields.io/badge/MySQL-8.0-orange) ![Python](https://img.shields.io/badge/Python-3.7+-green) ![Status](https://img.shields.io/badge/Status-Active-success)

## 🎯 Demostración en Vivo

**🌐 URL del Repositorio:** https://github.com/JerssonF/sistema-piscicola

## 🐟 Características Principales

- **🔐 Sistema de Autenticación**: Login seguro con validación de usuarios
- **📊 Dashboard Interactivo**: Vista general del sistema con navegación intuitiva
- **📝 Gestión Completa de Formularios**:
  - 🍽️ Formulario de Alimentos
  - 📦 Formulario de Ingreso de Alimentos  
  - 🔬 Formulario de Muestreo
  - ⚗️ Formulario de Parámetros
  - 🌱 Formulario de Siembra
- **📈 Sistema de Informes Avanzado**: Consulta y visualización de datos con filtros inteligentes
- **🎨 Interfaz Premium**: Diseño moderno con efectos glass, máxima transparencia y backdrop-filter blur

## 🚀 Tecnologías Utilizadas

- **Backend**: Flask (Python 3.7+)
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de Datos**: MySQL con XAMPP
- **Estilos**: CSS personalizado con efectos glass avanzados
- **Iconos**: Font Awesome
- **Efectos Visuales**: backdrop-filter blur, rgba transparency

## 📁 Estructura del Proyecto

```
piscicola/
├── app.py                              # Aplicación principal Flask
├── static/
│   ├── styles.css                      # Estilos con efectos glass premium
│   └── images/
│       └── fondo.jpeg                  # Imagen de fondo consistente
├── templates/
│   ├── dashboard.html                  # Panel principal
│   ├── formulario_alimentos.html       # Formulario de alimentos
│   ├── formulario_ingreso_alimento.html # Ingreso de alimentos
│   ├── formulario_muestreo.html        # Formulario de muestreo
│   ├── formulario_informes_final.html  # Sistema de informes (PRINCIPAL)
│   ├── index.html                      # Página de inicio
│   └── login.html                      # Página de login
├── .gitignore                          # Archivos excluidos del repositorio
└── README.md                           # Documentación del proyecto
```

## 🛠️ Instalación y Configuración

### 1. **Prerrequisitos**
```bash
# Instalar Python 3.7+
# Instalar XAMPP (MySQL + Apache)
```

### 2. **Clonar el repositorio**
```bash
git clone https://github.com/JerssonF/sistema-piscicola.git
cd sistema-piscicola
```

### 3. **Instalar dependencias**
```bash
pip install flask mysql-connector-python
```

### 4. **Configurar XAMPP/MySQL**
- Iniciar XAMPP Control Panel
- Activar Apache y MySQL
- Crear base de datos `piscicola`
- Verificar conexión en puerto 3306

### 5. **Ejecutar la aplicación**
```bash
python app.py
```

### 6. **Acceder al sistema**
- URL: `http://localhost:5000`
- 👤 Usuario: `admin`
- 🔑 Contraseña: `admin123`

## 🗃️ Base de Datos

### Tablas Principales:

| Tabla | Descripción | Campos Principales |
|-------|-------------|-------------------|
| **alimento** | Registros de alimentación | fecha, frecuencia_toma, estanque_celda, referencia_alimento, cantidad_alimento, mortalidad |
| **muestreo** | Datos de muestreos | fecha, frecuencia_toma, especie, biomasa, estanque_celda, peces, peso_promedio_g |
| **parametros** | Parámetros del agua | fecha, temperatura, ph, oxigeno_disuelto, amonio, nitritos |
| **siembra** | Información de siembras | fecha, especie, cantidad_peces, peso_promedio, estanque_celda |
| **usuarios** | Gestión de acceso | username, password |

## ✨ Funcionalidades Destacadas

### 🎯 Sistema de Informes (Principal)
- ✅ **Filtros Avanzados**: Por tipo de formulario, fechas y estanque
- ✅ **Visualización Premium**: Tablas con efectos glass y máxima transparencia
- ✅ **Búsqueda Inteligente**: Consultas optimizadas con parámetros dinámicos
- ✅ **Interfaz Fluida**: Sin movimiento de contenedores durante búsquedas

### 🎨 Diseño Visual
- ✅ **Efectos Glass**: backdrop-filter blur con valores optimizados (15px-25px)
- ✅ **Transparencia Máxima**: rgba values desde 0.20 hasta 0.45
- ✅ **Consistencia Visual**: Fondo unificado en todo el sistema
- ✅ **Responsive Design**: Adaptable a diferentes dispositivos

### 🔄 Gestión de Datos
- ✅ **CRUD Completo**: Crear, leer, actualizar datos
- ✅ **Validación de Formularios**: Controles de entrada robustos
- ✅ **Conexión Estable**: Manejo optimizado de conexiones MySQL
- ✅ **Mensajes de Estado**: Feedback visual para todas las operaciones

## 🎮 Guía de Uso

### 1. **Acceso al Sistema**
   - Ingresar credenciales en `/login`
   - Navegación automática al dashboard

### 2. **Registro de Datos**
   - Usar formularios específicos para cada tipo de registro
   - Completar campos requeridos
   - Confirmar guardado con modales

### 3. **Consulta de Informes**
   - Acceder a "Formulario de Informes"
   - Seleccionar tipo de formulario
   - Aplicar filtros de fecha/estanque
   - Visualizar resultados en tabla glass

## 🔧 Configuración Avanzada

### Variables de Entorno
```python
# En app.py
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'piscicola'
MYSQL_PORT = 3306
```

### Personalización de Estilos
```css
/* Efectos glass personalizables en static/styles.css */
.glass-container {
    background: rgba(255,255,255,0.30);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.2);
}
```

## 🚨 Solución de Problemas

### ❌ Error de Conexión MySQL
```bash
# Verificar estado de MySQL en XAMPP
# Comprobar puerto 3306
netstat -an | findstr :3306
```

### ❌ Tablas No Encontradas
```sql
-- Crear tablas manualmente si es necesario
USE piscicola;
SHOW TABLES;
```

### ❌ Problemas de Transparencia
```css
/* Ajustar valores de backdrop-filter en styles.css */
backdrop-filter: blur(20px); /* Aumentar para más nitidez */
```

## 📊 Estadísticas del Proyecto

![GitHub repo size](https://img.shields.io/github/repo-size/JerssonF/sistema-piscicola)
![GitHub last commit](https://img.shields.io/github/last-commit/JerssonF/sistema-piscicola)
![GitHub issues](https://img.shields.io/github/issues/JerssonF/sistema-piscicola)

- **📁 Archivos:** 42+ archivos organizados
- **📝 Líneas de código:** 7,500+ líneas
- **🎨 Templates:** 12 plantillas HTML
- **📊 Formularios:** 5 formularios completos
- **🗄️ Tablas BD:** 5 tablas principales

## 🤝 Contribuir

1. **Fork** el proyecto
2. **Crear rama** para feature (`git checkout -b feature/NewFeature`)
3. **Commit** cambios (`git commit -m 'Add NewFeature'`)
4. **Push** a la rama (`git push origin feature/NewFeature`)
5. **Abrir Pull Request**

## 📞 Contacto

**Desarrollador:** JerssonF  
**GitHub:** [@JerssonF](https://github.com/JerssonF)

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Ver archivo `LICENSE` para más detalles.

## 🏆 Reconocimientos

- **Flask Framework** por la robustez del backend
- **Font Awesome** por los iconos
- **MySQL** por la gestión de base de datos
- **CSS Glass Effects** por la interfaz moderna

---

<div align="center">
  <h3>🐟 Tecnología Flask + Diseño Premium Glass Effects © 2025</h3>
  <p>
    <a href="https://github.com/JerssonF/sistema-piscicola">⭐ Dale una estrella si te gustó el proyecto</a>
  </p>
</div>
