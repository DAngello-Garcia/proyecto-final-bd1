-- MySQL Script generated by MySQL Workbench
-- Thu Apr 25 23:20:08 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering
SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS,
  UNIQUE_CHECKS = 0;
SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS,
  FOREIGN_KEY_CHECKS = 0;
SET @OLD_SQL_MODE = @@SQL_MODE,
  SQL_MODE = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
-- -----------------------------------------------------
-- Schema libreria
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema libreria
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `libreria` DEFAULT CHARACTER SET utf8;
USE `libreria`;
ALTER DATABASE `libreria` CHARACTER SET utf8 COLLATE utf8_unicode_ci;
-- -----------------------------------------------------
-- Table `libreria`.`Pais`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Pais` (
  `idPais` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  PRIMARY KEY (`idPais`)
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Departamento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Departamento` (
  `idDepartamento` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `id_pais` INT NULL,
  PRIMARY KEY (`idDepartamento`),
  INDEX `id_pais_idx` (`id_pais` ASC),
  CONSTRAINT `id_pais_dept` FOREIGN KEY (`id_pais`) REFERENCES `libreria`.`Pais` (`idPais`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Ciudad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Ciudad` (
  `idCiudad` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `id_dpto` INT NULL,
  PRIMARY KEY (`idCiudad`),
  INDEX `id_dpto_idx` (`id_dpto` ASC),
  CONSTRAINT `id_dpto_ciu` FOREIGN KEY (`id_dpto`) REFERENCES `libreria`.`Departamento` (`idDepartamento`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Cliente` (
  `idCliente` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NULL,
  `fecha_nacimiento` DATE NULL,
  `direccion` VARCHAR(255) NULL,
  `telefono` VARCHAR(45) NULL,
  `id_ciudad` INT NULL,
  `username` VARCHAR(16) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  PRIMARY KEY (`idCliente`),
  UNIQUE INDEX `idCliente_UNIQUE` (`idCliente` ASC),
  INDEX `id_ciudad_idx` (`id_ciudad` ASC),
  CONSTRAINT `id_ciudad_cli` FOREIGN KEY (`id_ciudad`) REFERENCES `libreria`.`Ciudad` (`idCiudad`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Editorial`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Editorial` (
  `idEditorial` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `id_pais` INT NULL,
  `telefono` VARCHAR(45) NULL,
  `email` VARCHAR(255) NULL,
  `sitio_web` VARCHAR(255) NULL,
  PRIMARY KEY (`idEditorial`),
  INDEX `id_pais_idx` (`id_pais` ASC),
  CONSTRAINT `id_pais_editorial` FOREIGN KEY (`id_pais`) REFERENCES `libreria`.`Pais` (`idPais`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Dimensiones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Dimensiones` (
  `idDimensiones` INT NOT NULL AUTO_INCREMENT,
  `alto` DECIMAL(4, 2) NULL,
  `ancho` DECIMAL(4, 2) NULL,
  `largo` DECIMAL(4, 2) NULL,
  PRIMARY KEY (`idDimensiones`)
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Libro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Libro` (
  `idLibro` INT NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(255) NULL,
  `ISBN` VARCHAR(45) NULL,
  `fecha_publicacion` INT NULL,
  `id_editorial` INT NULL,
  `precio` DECIMAL(10, 2) NULL,
  `cantidad_disponible` INT NULL,
  `sinopsis` TEXT NULL,
  `numero_paginas` INT NULL,
  `idioma` VARCHAR(45) NULL,
  `peso` DECIMAL(10, 2) NULL,
  `id_dimensiones` INT NULL,
  PRIMARY KEY (`idLibro`),
  INDEX `id_editorial_idx` (`id_editorial` ASC),
  INDEX `id_dimensiones_idx` (`id_dimensiones` ASC),
  CONSTRAINT `id_editorial_libro` FOREIGN KEY (`id_editorial`) REFERENCES `libreria`.`Editorial` (`idEditorial`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_dimensiones_libro` FOREIGN KEY (`id_dimensiones`) REFERENCES `libreria`.`Dimensiones` (`idDimensiones`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Autor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Autor` (
  `idAutor` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `fecha_nacimiento` DATE NULL,
  `fecha_defuncion` DATE NULL,
  `biografia` TEXT NULL,
  `id_pais` INT NULL,
  PRIMARY KEY (`idAutor`),
  INDEX `id_pais_idx` (`id_pais` ASC),
  CONSTRAINT `id_pais_autor` FOREIGN KEY (`id_pais`) REFERENCES `libreria`.`Pais` (`idPais`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Cargo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Cargo` (
  `idCargo` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `salario` DECIMAL(10, 2) NULL,
  PRIMARY KEY (`idCargo`)
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Sucursal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Sucursal` (
  `idSucursal` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `direccion` VARCHAR(255) NULL,
  `telefono` VARCHAR(45) NULL,
  `email` VARCHAR(255) NULL,
  `id_ciudad` INT NULL,
  PRIMARY KEY (`idSucursal`),
  INDEX `id_ciudad_idx` (`id_ciudad` ASC),
  CONSTRAINT `id_ciudad_sucursal` FOREIGN KEY (`id_ciudad`) REFERENCES `libreria`.`Ciudad` (`idCiudad`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Empleado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Empleado` (
  `idEmpleado` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `fecha_nacimiento` DATE NULL,
  `email` VARCHAR(255) NULL,
  `telefono` VARCHAR(45) NULL,
  `direccion` VARCHAR(255) NULL,
  `id_sucursal` INT NULL,
  `id_ciudad` INT NULL,
  `id_cargo` INT NULL,
  `fecha_contratacion` DATE NULL,
  `username` VARCHAR(16) NULL,
  `password` VARCHAR(255) NULL,
  PRIMARY KEY (`idEmpleado`),
  INDEX `id_ciudad_idx` (`id_ciudad` ASC),
  INDEX `id_cargo_idx` (`id_cargo` ASC),
  INDEX `id_sucursal_idx` (`id_sucursal` ASC),
  CONSTRAINT `id_ciudad_emple` FOREIGN KEY (`id_ciudad`) REFERENCES `libreria`.`Ciudad` (`idCiudad`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_cargo_emple` FOREIGN KEY (`id_cargo`) REFERENCES `libreria`.`Cargo` (`idCargo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_sucursal_emple` FOREIGN KEY (`id_sucursal`) REFERENCES `libreria`.`Sucursal` (`idSucursal`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Pedido` (
  `idPedido` INT NOT NULL AUTO_INCREMENT,
  `id_cliente` INT NULL,
  `id_empleado` INT NULL,
  `fecha` TIMESTAMP NULL,
  `total` DECIMAL(10, 2) NULL,
  PRIMARY KEY (`idPedido`),
  INDEX `id_cliente_idx` (`id_cliente` ASC),
  INDEX `id_empleado_idx` (`id_empleado` ASC),
  CONSTRAINT `id_cliente_pedido` FOREIGN KEY (`id_cliente`) REFERENCES `libreria`.`Cliente` (`idCliente`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_empleado_pedido` FOREIGN KEY (`id_empleado`) REFERENCES `libreria`.`Empleado` (`idEmpleado`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Genero`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Genero` (
  `idGenero` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  PRIMARY KEY (`idGenero`)
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Presentacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Presentacion` (
  `idPresentacion` INT NOT NULL AUTO_INCREMENT,
  `presentacion` VARCHAR(45) NULL,
  PRIMARY KEY (`idPresentacion`)
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`MetodoPago`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`MetodoPago` (
  `idMetodoPago` INT NOT NULL AUTO_INCREMENT,
  `metodo` VARCHAR(45) NULL,
  PRIMARY KEY (`idMetodoPago`)
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Factura`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Factura` (
  `idFactura` INT NOT NULL AUTO_INCREMENT,
  `id_pedido` INT NULL,
  `id_cliente` INT NULL,
  `fechaEmision` TIMESTAMP NULL,
  `total` DECIMAL(10, 2) NULL,
  `fechaPago` TIMESTAMP NULL,
  `id_metodoPago` INT NULL,
  PRIMARY KEY (`idFactura`),
  INDEX `id_cliente_idx` (`id_cliente` ASC),
  INDEX `id_pedido_idx` (`id_pedido` ASC),
  INDEX `id_metodoPago_idx` (`id_metodoPago` ASC),
  CONSTRAINT `id_cliente_factura` FOREIGN KEY (`id_cliente`) REFERENCES `libreria`.`Cliente` (`idCliente`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_pedido_factura` FOREIGN KEY (`id_pedido`) REFERENCES `libreria`.`Pedido` (`idPedido`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_metodoPago_factura` FOREIGN KEY (`id_metodoPago`) REFERENCES `libreria`.`MetodoPago` (`idMetodoPago`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`LibroGenero`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`LibroGenero` (
  `id_libro` INT NULL,
  `id_genero` INT NULL,
  INDEX `id_libro_idx` (`id_libro` ASC),
  INDEX `id_genero_idx` (`id_genero` ASC),
  CONSTRAINT `id_libro_libroGenero` FOREIGN KEY (`id_libro`) REFERENCES `libreria`.`Libro` (`idLibro`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_genero_libroGenero` FOREIGN KEY (`id_genero`) REFERENCES `libreria`.`Genero` (`idGenero`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`LibroPresentacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`LibroPresentacion` (
  `id_libro` INT NULL,
  `id_presentacion` INT NULL,
  INDEX `id_libro_idx` (`id_libro` ASC),
  INDEX `id_presentacion_idx` (`id_presentacion` ASC),
  CONSTRAINT `id_libro_libroPresen` FOREIGN KEY (`id_libro`) REFERENCES `libreria`.`Libro` (`idLibro`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_presentacion_libroPresen` FOREIGN KEY (`id_presentacion`) REFERENCES `libreria`.`Presentacion` (`idPresentacion`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`DetallePedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`DetallePedido` (
  `id_pedido` INT NULL,
  `id_libro` INT NULL,
  `cantidad` INT NULL,
  `precio_unitario` DECIMAL(10, 2) NULL,
  `subtotal` DECIMAL(10, 2) NULL,
  INDEX `id_pedido_idx` (`id_pedido` ASC),
  INDEX `id_libro_idx` (`id_libro` ASC),
  CONSTRAINT `id_pedido_detallePedido` FOREIGN KEY (`id_pedido`) REFERENCES `libreria`.`Pedido` (`idPedido`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_libro_detallePedido` FOREIGN KEY (`id_libro`) REFERENCES `libreria`.`Libro` (`idLibro`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`EstadoPedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`EstadoPedido` (
  `idEstadoPedido` INT NOT NULL AUTO_INCREMENT,
  `estado` VARCHAR(45) NULL,
  PRIMARY KEY (`idEstadoPedido`)
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`HistorialEstadoPedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`HistorialEstadoPedido` (
  `id_pedido` INT NULL,
  `id_estado` INT NULL,
  `fecha` TIMESTAMP NULL,
  INDEX `id_pedido_idx` (`id_pedido` ASC),
  INDEX `id_estado_idx` (`id_estado` ASC),
  CONSTRAINT `id_pedido_historialEstaPed` FOREIGN KEY (`id_pedido`) REFERENCES `libreria`.`Pedido` (`idPedido`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_estado_historialEstaPed` FOREIGN KEY (`id_estado`) REFERENCES `libreria`.`EstadoPedido` (`idEstadoPedido`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`AutorLibro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`AutorLibro` (
  `id_libro` INT NOT NULL,
  `id_autor` INT NOT NULL,
  PRIMARY KEY (`id_libro`, `id_autor`),
  INDEX `id_autor_idx` (`id_autor` ASC),
  CONSTRAINT `id_libro_autorLibr` FOREIGN KEY (`id_libro`) REFERENCES `libreria`.`Libro` (`idLibro`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_autor_autorLibr` FOREIGN KEY (`id_autor`) REFERENCES `libreria`.`Autor` (`idAutor`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`Proveedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`Proveedor` (
  `idProveedor` INT NOT NULL,
  `nombre` VARCHAR(45) NULL,
  `direccion` VARCHAR(45) NULL,
  `id_ciudad` INT NULL,
  `telefono` VARCHAR(45) NULL,
  `email` VARCHAR(255) NULL,
  PRIMARY KEY (`idProveedor`)
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`PedidosProveedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`PedidosProveedor` (
  `idPedidosProveedor` INT NOT NULL,
  `id_sucursal` INT NULL,
  `fecha` TIMESTAMP NULL,
  `total` DECIMAL(10, 2) NULL,
  `id_proveedor` INT NULL,
  PRIMARY KEY (`idPedidosProveedor`),
  INDEX `id_sucursal_idx` (`id_sucursal` ASC),
  INDEX `id_proveedor_idx` (`id_proveedor` ASC),
  CONSTRAINT `id_sucursal_pedidosProve` FOREIGN KEY (`id_sucursal`) REFERENCES `libreria`.`Sucursal` (`idSucursal`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_proveedor_pedidosProve` FOREIGN KEY (`id_proveedor`) REFERENCES `libreria`.`Proveedor` (`idProveedor`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `libreria`.`DetallePedidosProveedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `libreria`.`DetallePedidosProveedor` (
  `id_pedidoProveedor` INT NOT NULL,
  `id_libro` INT NOT NULL,
  `cantidad` INT NULL,
  `precio_unitario` DECIMAL(10, 2) NULL,
  `subtotal` DECIMAL(10, 2) NULL,
  PRIMARY KEY (`id_pedidoProveedor`, `id_libro`),
  INDEX `id_libro_idx` (`id_libro` ASC),
  CONSTRAINT `id_pedidoProveedor_detallesPediProv` FOREIGN KEY (`id_pedidoProveedor`) REFERENCES `libreria`.`PedidosProveedor` (`idPedidosProveedor`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_libro_detallesPediProv` FOREIGN KEY (`id_libro`) REFERENCES `libreria`.`Libro` (`idLibro`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
SET SQL_MODE = @OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS;
-- Inserción de datos en la tabla Pais
INSERT INTO `libreria`.`Pais` (`nombre`)
VALUES ('Argentina'),
  ('España'),
  ('México'),
  ('Grecia');
-- Inserción de datos en la tabla Departamento
INSERT INTO `libreria`.`Departamento` (`nombre`, `id_pais`)
VALUES ('Buenos Aires', 1),
  ('Madrid', 2),
  ('Ciudad de México', 3);
-- Inserción de datos en la tabla Ciudad
INSERT INTO `libreria`.`Ciudad` (`nombre`, `id_dpto`)
VALUES ('La Plata', 1),
  ('Barcelona', 2),
  ('Guadalajara', 3);
-- Inserción de datos en la tabla Cliente
INSERT INTO `libreria`.`Cliente` (
    `nombre`,
    `apellido`,
    `fecha_nacimiento`,
    `direccion`,
    `telefono`,
    `id_ciudad`,
    `username`,
    `email`,
    `password`
  )
VALUES (
    'Juan',
    'Perez',
    '1990-05-15',
    'Calle 123',
    '123456789',
    1,
    'juanp',
    'juanp@cliente.com',
    '$2b$12$yp8U5JSnSUuzuwXQqf85K.rfZuWJXN/KQaihn5RCfzJgkTVW24wly'
  ),
  (
    'María',
    'González',
    '1985-08-20',
    'Av. Principal 456',
    '987654321',
    2,
    'mariag',
    'mariag@cliente.com',
    '$2b$12$yp8U5JSnSUuzuwXQqf85K.rfZuWJXN/KQaihn5RCfzJgkTVW24wly'
  );
-- Inserción de datos en la tabla Editorial
INSERT INTO `libreria`.`Editorial` (
    `nombre`,
    `id_pais`,
    `telefono`,
    `email`,
    `sitio_web`
  )
VALUES (
    'Editorial Argenta',
    1,
    '1122334455',
    'info@editorialargenta.com',
    'www.editorialargenta.com'
  ),
  (
    'Editorial Española',
    2,
    '6677889900',
    'info@editorialespanola.com',
    'www.editorialespanola.com'
  );
-- Inserción de datos en la tabla Dimensiones
INSERT INTO `libreria`.`Dimensiones` (`alto`, `ancho`, `largo`)
VALUES (20.5, 15.2, 3.8),
  (30.0, 22.0, 4.5);
-- Inserción de datos en la tabla Libro
INSERT INTO `libreria`.`Libro` (
    `titulo`,
    `ISBN`,
    `fecha_publicacion`,
    `id_editorial`,
    `precio`,
    `cantidad_disponible`,
    `sinopsis`,
    `numero_paginas`,
    `idioma`,
    `peso`,
    `id_dimensiones`
  )
VALUES (
    'El Quijote',
    '9788437610197',
    1605,
    2,
    25.99,
    100,
    'Novela sobre las aventuras de Don Quijote y Sancho Panza',
    800,
    'Español',
    1.5,
    1
  ),
  (
    'Cien años de soledad',
    '9788497592208',
    1967,
    1,
    30.50,
    80,
    'Relato sobre la familia Buendía en Macondo',
    432,
    'Español',
    1.2,
    2
  ),
  (
    'Diálogos',
    '9789706665706',
    2008,
    1,
    26.95,
    50,
    'En Fedro o de la belleza, Sócrates inicia a su joven amigo en los misterios de la eterna belleza; le enseña a alimentar su inteligencia con lo verdadero, lo bello y lo bueno, para merecer un día tomar sus alas y volar de nuevo a la patria de las almas...',
    221,
    'Español',
    1,
    1
  );
-- Inserción de datos en la tabla Autor
INSERT INTO `libreria`.`Autor` (
    `nombre`,
    `apellido`,
    `fecha_nacimiento`,
    `fecha_defuncion`,
    `biografia`,
    `id_pais`
  )
VALUES (
    'Miguel',
    'de Cervantes',
    '1547-09-29',
    '1616-04-22',
    'Autor de "El Quijote"',
    1
  ),
  (
    'Gabriel',
    'García Márquez',
    '1927-03-06',
    '2014-04-17',
    'Autor de "Cien años de soledad"',
    3
  ),
  (
    'Platón',
    '',
    '428-01-01',
    '348-01-01',
    'Platón fue un filósofo griego que fue discípulo de Sócrates y maestro de Aristóteles. Fundó la Academia de Atenas, la primera institución de educación superior del mundo occidental. Es conocido por sus diálogos filosóficos y por sus ideas sobre la teoría de las formas y la justicia.',
    4
  );
-- Inserción de datos en la tabla Cargo
INSERT INTO `libreria`.`Cargo` (`nombre`, `salario`)
VALUES ('Vendedor', 1500.00),
  ('Gerente', 3000.00);
-- Inserción de datos en la tabla Sucursal
INSERT INTO `libreria`.`Sucursal` (
    `nombre`,
    `direccion`,
    `telefono`,
    `email`,
    `id_ciudad`
  )
VALUES (
    'Sucursal Centro',
    'Av. Principal 789',
    '5551234',
    'info@sucursalcentro.com',
    1
  ),
  (
    'Sucursal Norte',
    'Calle Norte 456',
    '5555678',
    'info@sucursalnorte.com',
    3
  );
-- Inserción de datos en la tabla Empleado
INSERT INTO `libreria`.`Empleado` (
    `nombre`,
    `apellido`,
    `fecha_nacimiento`,
    `email`,
    `telefono`,
    `direccion`,
    `id_sucursal`,
    `id_ciudad`,
    `id_cargo`,
    `fecha_contratacion`,
    `username`,
    `password`
  )
VALUES (
    'Pedro',
    'Martínez',
    '1980-10-10',
    'pedro@libreria.com',
    '3331234',
    'Calle Sur 123',
    1,
    1,
    2,
    '2020-01-15',
    'pedrom',
    '$2b$12$yp8U5JSnSUuzuwXQqf85K.rfZuWJXN/KQaihn5RCfzJgkTVW24wly'
  ),
  (
    'Ana',
    'López',
    '1992-07-05',
    'ana@libreria.com',
    '4445678',
    'Av. Este 456',
    2,
    3,
    1,
    '2021-03-20',
    'anl',
    '$2b$12$yp8U5JSnSUuzuwXQqf85K.rfZuWJXN/KQaihn5RCfzJgkTVW24wly'
  );
INSERT INTO `libreria`.`AutorLibro` (`id_libro`, `id_autor`)
VALUES (1, 1),
  (2, 2),
  (3, 3);
-- Inserción de datos en la tabla Genero
INSERT INTO `libreria`.`Genero` (`nombre`)
VALUES ('Filosofía'),
  ('Novela');
-- Inserción de datos en la tabla Presentacion
INSERT INTO `libreria`.`Presentacion` (`presentacion`)
VALUES ('Tapa dura'),
  ('Tapa blanda');
-- Inserción de datos en la tabla MetodoPago
INSERT INTO `libreria`.`MetodoPago` (`metodo`)
VALUES ('Tarjeta de crédito'),
  ('Transferencia bancaria');
INSERT INTO `libreria`.`LibroGenero` (`id_libro`, `id_genero`)
VALUES (1, 2),
  (2, 2),
  (3, 1);
INSERT INTO `libreria`.`LibroPresentacion` (`id_libro`, `id_presentacion`)
VALUES (1, 2),
  (2, 2),
  (3, 1);
-- Inserción de datos en la tabla EstadoPedido
INSERT INTO `libreria`.`EstadoPedido` (`estado`)
VALUES ('En proceso'),
  ('Enviado'),
  ('Entregado');
-- Inserción de datos en la tabla AutorLibro
-- Inserción de datos en la tabla Proveedor
INSERT INTO `libreria`.`Proveedor` (
    `idProveedor`,
    `nombre`,
    `direccion`,
    `id_ciudad`,
    `telefono`,
    `email`
  )
VALUES (
    1,
    'Editorial XYZ',
    'Calle Proveedores 123',
    1,
    '5556789',
    'info@editorialxyz.com'
  );
-- Inserción de datos en la tabla PedidosProveedor
INSERT INTO `libreria`.`PedidosProveedor` (
    `idPedidosProveedor`,
    `id_sucursal`,
    `fecha`,
    `total`,
    `id_proveedor`
  )
VALUES (1, 1, '2024-04-28 10:00:00', 500.00, 1);
-- Inserción de datos en la tabla DetallePedidosProveedor
-- INSERT INTO `libreria`.`DetallePedidosProveedor` (
--     `id_pedidoProveedor`,
--     `id_libro`,
--     `cantidad`,
--     `precio_unitario`,
--     `subtotal`
--   )
-- VALUES (1, 1, 10, 20.00, 200.00),
--   (1, 2, 8, 25.00, 200.00);