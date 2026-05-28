CREATE DATABASE IF NOT EXISTS ciber;
USE ciber;
CREATE TABLE clases(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    idioma VARCHAR(255) NOT NULL,
    nivel VARCHAR(255) NOT NULL,
    precio DECIMAL(9,2) NOT NULL,
	foto VARCHAR(255)
);
CREATE TABLE comentarios(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL
);
CREATE TABLE usuarios(
	usuario VARCHAR(100) NOT NULL PRIMARY KEY,
    clave VARCHAR(255) NOT NULL,
    perfil VARCHAR(100) NOT NULL,
    estado VARCHAR(50) DEFAULT 'activo',
    numeroAccesosErroneo INT DEFAULT 0,
    fechaUltimoAcceso DATE
);
INSERT INTO `usuarios` (`usuario`, `clave`, `perfil`, `estado`, `numeroAccesosErroneo`) VALUES ('root', '$2b$10$1234567890123456789012', 'admin', 'activo', 0);

