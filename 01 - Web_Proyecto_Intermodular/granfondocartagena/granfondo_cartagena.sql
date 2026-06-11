-- 1. CREACIÓN DE LA BASE DE DATOS
CREATE DATABASE granfondo_cartagena;
USE granfondo_cartagena;

-- 2. TABLA DE CATEGORÍAS (Para la carga dinámica de rutas y precios)
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    distancia VARCHAR(50) NOT NULL,
    desnivel VARCHAR(50) NOT NULL,
    precio DECIMAL(6,2) NOT NULL
);

-- 3. TABLA DE PARTICIPANTES (Gestión y almacenamiento de inscripciones)
CREATE TABLE participantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    dni VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL,
    id_categoria INT NOT NULL,
    alojamiento VARCHAR(2) NOT NULL DEFAULT 'No',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id)
);

-- 4. INSERCIÓN DE DATOS INICIALES (Circuitos inspirados en Mallorca 312 y Reynolds)
INSERT INTO categorias (nombre, distancia, desnivel, precio) VALUES
('Gran Fondo Perico Delgado', '180 Km', '3500 m', 85.00),
('Medio Fondo Miguel Induráin', '120 Km', '2100 m', 65.00),
('Mini Fondo Puertos de Mazarrón', '75 Km', '1100 m', 45.00);

-- 5. PROTOCOLO DE USUARIOS DEL SISTEMA, SEGURIDAD Y PRIVILEGIOS

-- Crear Usuario de conexión para la Aplicación Web (Permisos de inserción, lectura y borrado)
CREATE USER 'cliente_granfondo_ct'@'localhost' IDENTIFIED BY 'cl5ent4.!Reynolds1980';
-- Asignar los permisos específicos (Lectura, Inserción y Borrado) sobre la Base de Datos
GRANT SELECT, INSERT, DELETE ON granfondo_cartagena.* TO 'cliente_granfondo_ct'@'localhost';
-- Aplicar los cambios en el sistema de permisos
FLUSH PRIVILEGES;
