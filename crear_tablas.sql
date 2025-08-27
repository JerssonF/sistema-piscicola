-- Script para crear todas las tablas de la base de datos piscicola
-- Ejecutar este script en MySQL Workbench o línea de comandos

-- Usar la base de datos piscicola
USE piscicola;

-- Tabla para el formulario de alimentos
CREATE TABLE IF NOT EXISTS alimento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    frecuencia_toma VARCHAR(100),
    estanque_celda VARCHAR(50),
    referencia_alimento VARCHAR(100),
    cantidad_alimento DECIMAL(10,2),
    mortalidad INT,
    causa_mortalidad TEXT,
    acciones_correctivas TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para el formulario de ingreso de alimentos
CREATE TABLE IF NOT EXISTS ingreso_alimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    ingreso_comida VARCHAR(100),
    cantidad DECIMAL(10,2),
    transporte VARCHAR(100),
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para el formulario de muestreo
CREATE TABLE IF NOT EXISTS muestreo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    frecuencia_toma VARCHAR(100),
    especie VARCHAR(100),
    biomasa DECIMAL(10,2),
    estanque_celda VARCHAR(50),
    peces INT,
    peso_promedio_g DECIMAL(10,2),
    promedio_total_g DECIMAL(10,2),
    acciones_correctivas TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mostrar las tablas creadas
SHOW TABLES;

-- Verificar la estructura de las tablas
DESCRIBE alimento;
DESCRIBE ingreso_alimentos;
DESCRIBE muestreo;
