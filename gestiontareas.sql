-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-06-2024 a las 18:30:57
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gestiontareas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas`
--

CREATE TABLE `tareas` (
  `IDtarea` int(11) NOT NULL,
  `nombretar` varchar(200) NOT NULL,
  `fechainicio` date DEFAULT NULL,
  `fechafin` date DEFAULT NULL,
  `estado` enum('por asignar','en proceso','terminado') DEFAULT NULL,
  `Id_Usuario1` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tareas`
--

INSERT INTO `tareas` (`IDtarea`, `nombretar`, `fechainicio`, `fechafin`, `estado`, `Id_Usuario1`) VALUES
(1, 'Pescar', '2024-06-04', '2024-06-10', 'terminado', 9),
(2, 'Cocinar', '2024-06-06', '2024-06-21', 'terminado', 10),
(18, 'Documentacion', '2024-05-19', '2024-05-31', 'en proceso', 9),
(19, 'Nadar', '2024-06-04', '2024-06-10', 'terminado', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `idUsuarios` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `apellido` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `usuario` varchar(255) DEFAULT NULL,
  `contraseña` varchar(255) DEFAULT NULL,
  `rol` enum('usuario','admin') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`idUsuarios`, `nombre`, `apellido`, `email`, `usuario`, `contraseña`, `rol`) VALUES
(9, 'Maria', 'Maldonado', 'mp@gmail.com', 'mpmaldo', 'scrypt:32768:8:1$H9FejRqXTEBiOeGj$70e9607f8813329ec6ddc7dd29244f2ca95032eca433be8369e0fc456652350be28f9a35a21692e742b0b8e284993e30d305a7c96b7b6f887d8d65a1ea8587fd', 'usuario'),
(10, 'santiago', 'fuquene', 'santiagomp@gmail.com', 'santimp\r\n', 'scrypt:32768:8:1$ddmlf11CxwtqbkVj$6d3ae5d39a3d63942963bd3a0d4dd2708e3879d94c9e33050c78c6aba97d880d2d48097f37646739f570e6ee32efd2b912d6cf05454807df1e58e9e2ce2a3427', 'admin'),
(11, 'Ryan ', 'Castro', 'Ryan@gmail.com', 'Ryan', 'scrypt:32768:8:1$Bwk1A7eyF4mOlHjE$51a992b53f991b57afa8a892c3983dace2148f8b488285aeca4c303ead3082b89aee3c1a626e63504fad783c86261da78dce81eaa3d5f7652aa95e91751eb1c1', 'admin');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`IDtarea`),
  ADD KEY `tareas_ibfk_1` (`Id_Usuario1`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`idUsuarios`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `tareas`
--
ALTER TABLE `tareas`
  MODIFY `IDtarea` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idUsuarios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD CONSTRAINT `tareas_ibfk_1` FOREIGN KEY (`Id_Usuario1`) REFERENCES `usuarios` (`idUsuarios`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
