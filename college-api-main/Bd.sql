-- Crear la base de datos parqueadero2
CREATE DATABASE IF NOT EXISTS parqueadero2;

-- Usar la base de datos parqueadero2
USE parqueadero2;

-- Primero crear todas las tablas que son referenciadas
-- 1. Crear la tabla para código
CREATE TABLE codigo (
    id_codigo INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Crear la tabla para tipo
CREATE TABLE tipo (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL
);

-- 3. Crear la tabla para bodega
CREATE TABLE bodega (
    id_bodega INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- 4. Crear la tabla para categoría
CREATE TABLE categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- 5. Crear la tabla para marca
CREATE TABLE marca (
    id_marca INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- 6. Crear la tabla para unidad de medida
CREATE TABLE unidad_medida (
    id_unidad_medida INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- Finalmente, crear la tabla productos que tiene las foreign keys
-- 7. Crear la tabla para productos
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    inventario INT DEFAULT 0,
    precio_venta DECIMAL(10, 2) NOT NULL,
    costo DECIMAL(10, 2) NOT NULL,
    codigo_id INT,
    tipo_id INT,
    bodega_id INT,
    categoria_id INT,
    marca_id INT,
    unidad_medida_id INT,
    FOREIGN KEY (codigo_id) REFERENCES codigo(id_codigo),
    FOREIGN KEY (tipo_id) REFERENCES tipo(id_tipo),
    FOREIGN KEY (bodega_id) REFERENCES bodega(id_bodega),
    FOREIGN KEY (categoria_id) REFERENCES categoria(id_categoria),
    FOREIGN KEY (marca_id) REFERENCES marca(id_marca),
    FOREIGN KEY (unidad_medida_id) REFERENCES unidad_medida(id_unidad_medida)
);