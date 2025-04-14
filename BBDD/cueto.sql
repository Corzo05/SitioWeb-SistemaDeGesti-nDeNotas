-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 14-04-2025 a las 20:37:41
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
-- Base de datos: `cueto`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administradores`
--

CREATE TABLE `administradores` (
  `ID` int(5) NOT NULL,
  `Nombre_apellido` varchar(100) NOT NULL,
  `Usuario` varchar(50) NOT NULL,
  `Contraseña` varchar(50) NOT NULL,
  `Rol` varchar(100) NOT NULL,
  `Materia` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `administradores`
--

INSERT INTO `administradores` (`ID`, `Nombre_apellido`, `Usuario`, `Contraseña`, `Rol`, `Materia`) VALUES
(1, 'Carmelo Boscán', 'Carmelo', 'VeKarmelo*', 'Jefe de Control de Estudios', 'No Aplica'),
(2, 'José Corzo', 'Jose', 'Jose*', 'Jefe de Control de Estudios', 'No Aplica'),
(3, 'Judith Contreras', 'Judith', 'VeJudith*', 'Docente', 'Biología'),
(4, 'Richard Salazar', 'Richard', 'VeRichard*', 'Docente', 'Matemática'),
(5, 'Hendrith Valbuena', 'Hendrith', 'VeHendrith*', 'Docente', 'Inglés'),
(6, 'Abraham Paradas', 'Abraham', 'Abraham3', 'Docente', 'Religión'),
(7, 'Eidy Hernández', 'Eidy', 'VeEidy*', 'Docente', 'GHC'),
(8, 'Luis Rojas', 'Luis', 'VeLuis*', 'Docente', 'Castellano'),
(9, 'Abraham Paradas', 'Abraham', 'VeAbrahan*', 'Docente', 'Computación');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `primer_lapso_a`
--

CREATE TABLE `primer_lapso_a` (
  `Nro` int(5) NOT NULL,
  `Nombre_completo` varchar(100) NOT NULL,
  `Sexo` varchar(5) NOT NULL,
  `Cedula` varchar(50) NOT NULL,
  `Castellano` int(10) NOT NULL,
  `Matematica` int(10) NOT NULL,
  `GHC` int(10) NOT NULL,
  `Religion` int(10) NOT NULL,
  `Biologia` int(10) NOT NULL,
  `Computacion` int(10) NOT NULL,
  `Ingles` int(10) NOT NULL,
  `Arte` int(10) NOT NULL,
  `Educacion_fisica` int(10) NOT NULL,
  `Promedio` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `primer_lapso_a`
--

INSERT INTO `primer_lapso_a` (`Nro`, `Nombre_completo`, `Sexo`, `Cedula`, `Castellano`, `Matematica`, `GHC`, `Religion`, `Biologia`, `Computacion`, `Ingles`, `Arte`, `Educacion_fisica`, `Promedio`) VALUES
(1, 'AGELVIS LAREZ VICTORIA VALENTINA', 'F', 'V-33885411', 20, 14, 15, 17, 11, 16, 18, 19, 19, 16.56),
(2, 'AU GUTIERREZ YULEYDIS YANASKI', 'F', 'V-34987023', 15, 14, 17, 18, 11, 12, 20, 14, 13, 14.89),
(3, 'BERMUDEZ SULBARAN ALCIBETH JOVANNA', 'F', 'V-31701110', 12, 19, 16, 17, 14, 13, 19, 10, 5, 12.89),
(4, 'BRACHO BARRIOSNUEVO SANTIAGO JAVIER', 'M', 'V-34980190', 20, 20, 13, 12, 15, 11, 14, 16, 17, 15.33),
(5, 'CHACIN FERNANDEZ CAMILA VICTORIA', 'F', 'V-3467098', 12, 15, 16, 15, 16, 18, 19, 20, 6, 15.22),
(6, 'CHIRINOS CHOURIO JEIBER JOSE', 'M', 'V-23876149', 13, 15, 11, 12, 15, 16, 17, 20, 20, 15.44),
(7, 'GARCIA SANCHEZ RASHEILY PAOLA', 'F', 'V-10560190', 13, 11, 15, 6, 8, 10, 15, 18, 11, 11.89),
(32, 'GONZALEZ ACEVEDO SANTIAGO JAVIER ', 'M', 'V-12098145', 12, 16, 18, 12, 16, 17, 19, 20, 20, 16.67),
(33, 'LAGUNA MORENO SOFIA VALENTINA', 'F', 'V-11089456', 12, 15, 11, 12, 17, 18, 19, 20, 20, 16.00),
(34, 'LEON GUERRA SOFIA VALENTINA', 'F', 'V-33109561', 13, 16, 18, 19, 20, 15, 11, 16, 20, 16.44),
(36, 'Prueba', 'M', 'V-345764654', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `primer_lapso_b`
--

CREATE TABLE `primer_lapso_b` (
  `Nro` int(5) NOT NULL,
  `Nombre_completo` varchar(100) NOT NULL,
  `Sexo` varchar(5) NOT NULL,
  `Cedula` varchar(50) NOT NULL,
  `Castellano` int(5) NOT NULL,
  `Matematica` int(5) NOT NULL,
  `GHC` int(5) NOT NULL,
  `Religion` int(5) NOT NULL,
  `Biologia` int(5) NOT NULL,
  `Computacion` int(5) NOT NULL,
  `Ingles` int(5) NOT NULL,
  `Arte` int(5) NOT NULL,
  `Educacion_fisica` int(5) NOT NULL,
  `Promedio` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `primer_lapso_b`
--

INSERT INTO `primer_lapso_b` (`Nro`, `Nombre_completo`, `Sexo`, `Cedula`, `Castellano`, `Matematica`, `GHC`, `Religion`, `Biologia`, `Computacion`, `Ingles`, `Arte`, `Educacion_fisica`, `Promedio`) VALUES
(1, 'BRICEÑO MONTIEL ROBINSON LUIS', 'M', 'V-13098098', 12, 19, 19, 19, 18, 20, 13, 5, 2, 14.11),
(2, 'CHANGANO RINCON ADRIANN ALEJANDRO', 'M', 'V-33455123', 12, 13, 16, 17, 13, 18, 14, 4, 9, 12.89),
(3, 'CHOURIO SOTO KEINER DANIEL', 'M', 'V-23937247', 12, 12, 11, 16, 17, 18, 19, 20, 14, 15.44),
(4, 'COLINA MILLAN ENMANUEL ANDRES', 'M', 'V-14987139', 13, 16, 16, 15, 10, 20, 16, 18, 20, 16.00),
(5, 'CUBILLAN CASTRO YULIANIS YULIETH', 'F', 'V-12095678', 13, 17, 18, 19, 10, 20, 17, 18, 20, 16.89),
(6, 'GIRADO BOHORQUEZ YEFRYD DE JESUS', 'M', 'V-11345876', 16, 16, 17, 19, 20, 19, 12, 14, 20, 17.00),
(7, 'JIMENEZ COLS ISABELLA LUCIA', 'F', 'V-1298421', 13, 10, 11, 17, 14, 15, 18, 20, 19, 15.22),
(8, 'LAMEDA ALVAREZ ANYIBEL VICTORIA ', 'F', 'V-11233455', 18, 16, 17, 20, 12, 14, 17, 28, 10, 16.89),
(9, 'LOBO PADRON YORMARY DE LOS ANGELES', 'F', 'V-7899880', 15, 20, 18, 19, 12, 17, 16, 15, 12, 16.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_estudiantes_a`
--

CREATE TABLE `registro_estudiantes_a` (
  `Nro` int(5) NOT NULL,
  `Nombre_completo` varchar(100) NOT NULL,
  `Sexo` varchar(5) NOT NULL,
  `Cedula` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `registro_estudiantes_a`
--

INSERT INTO `registro_estudiantes_a` (`Nro`, `Nombre_completo`, `Sexo`, `Cedula`) VALUES
(1, 'AGELVIS LAREZ VICTORIA VALENTINA', 'F', 'V-33885411'),
(2, 'AU GUTIERREZ YULEYDIS YANASKI', 'F', 'V-34987023'),
(3, 'BERMUDEZ SULBARAN ALCIBETH JOVANNA', 'F', 'V-31701110'),
(4, 'BRACHO BARRIOSNUEVO SANTIAGO JAVIER', 'M', 'V-34980190'),
(5, 'CHACIN FERNANDEZ CAMILA VICTORIA', 'F', 'V-3467098'),
(6, 'CHIRINOS CHOURIO JEIBER JOSE', 'M', 'V-23876149'),
(7, 'GARCIA SANCHEZ RASHEILY PAOLA', 'F', 'V-10560190'),
(32, 'GONZALEZ ACEVEDO SANTIAGO JAVIER ', 'M', 'V-12098145'),
(33, 'LAGUNA MORENO SOFIA VALENTINA', 'F', 'V-11089456'),
(34, 'LEON GUERRA SOFIA VALENTINA', 'F', 'V-33109561'),
(36, 'Prueba', 'M', 'V-345764654');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_estudiantes_b`
--

CREATE TABLE `registro_estudiantes_b` (
  `Nro` int(5) NOT NULL,
  `Nombre_completo` varchar(100) NOT NULL,
  `Sexo` varchar(5) NOT NULL,
  `Cedula` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `registro_estudiantes_b`
--

INSERT INTO `registro_estudiantes_b` (`Nro`, `Nombre_completo`, `Sexo`, `Cedula`) VALUES
(1, 'BRICEÑO MONTIEL ROBINSON LUIS', 'M', 'V-13098098'),
(2, 'CHANGANO RINCON ADRIANN ALEJANDRO', 'M', 'V-33455123'),
(3, 'CHOURIO SOTO KEINER DANIEL', 'M', 'V-23937247'),
(4, 'COLINA MILLAN ENMANUEL ANDRES', 'M', 'V-14987139'),
(5, 'CUBILLAN CASTRO YULIANIS YULIETH', 'F', 'V-12095678'),
(6, 'GIRADO BOHORQUEZ YEFRYD DE JESUS', 'M', 'V-11345876'),
(7, 'JIMENEZ COLS ISABELLA LUCIA', 'F', 'V-1298421'),
(8, 'LAMEDA ALVAREZ ANYIBEL VICTORIA ', 'F', 'V-11233455'),
(9, 'LOBO PADRON YORMARY DE LOS ANGELES', 'F', 'V-7899880');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seccion_a`
--

CREATE TABLE `seccion_a` (
  `Nro` int(9) NOT NULL,
  `Nombre_completo` varchar(100) NOT NULL,
  `Sexo` varchar(5) NOT NULL,
  `Cedula` varchar(50) NOT NULL,
  `Castellano` int(5) NOT NULL,
  `Matematica` int(5) NOT NULL,
  `GHC` int(5) NOT NULL,
  `Religion` int(5) NOT NULL,
  `Biologia` int(5) NOT NULL,
  `Computacion` int(5) NOT NULL,
  `Ingles` int(5) NOT NULL,
  `Arte` int(5) NOT NULL,
  `Educacion_fisica` int(5) NOT NULL,
  `Promedio` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `seccion_a`
--

INSERT INTO `seccion_a` (`Nro`, `Nombre_completo`, `Sexo`, `Cedula`, `Castellano`, `Matematica`, `GHC`, `Religion`, `Biologia`, `Computacion`, `Ingles`, `Arte`, `Educacion_fisica`, `Promedio`) VALUES
(1, 'AGELVIS LAREZ VICTORIA VALENTINA', 'F', 'V-33885411', 18, 16, 16, 16, 14, 15, 15, 12, 13, 15.00),
(2, 'AU GUTIERREZ YULEYDIS YANASKI', 'F', 'V-34987023', 13, 14, 15, 13, 11, 8, 12, 10, 13, 12.11),
(3, 'BERMUDEZ SULBARAN ALCIBETH JOVANNA', 'F', 'V-31701110', 12, 15, 15, 15, 15, 17, 19, 15, 10, 14.78),
(4, 'BRACHO BARRIOSNUEVO SANTIAGO JAVIER', 'M', 'V-34980190', 16, 18, 14, 16, 12, 13, 14, 18, 14, 15.00),
(5, 'CHACIN FERNANDEZ CAMILA VICTORIA', 'F', 'V-3467098', 14, 16, 15, 18, 15, 13, 11, 15, 14, 14.56),
(6, 'CHIRINOS CHOURIO JEIBER JOSE', 'M', 'V-23876149', 12, 11, 11, 15, 16, 17, 17, 17, 18, 14.89),
(7, 'GARCIA SANCHEZ RASHEILY PAOLA', 'F', 'V-10560190', 12, 12, 15, 13, 15, 12, 17, 16, 13, 13.89),
(32, 'GONZALEZ ACEVEDO SANTIAGO JAVIER ', 'M', 'V-12098145', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.00),
(33, 'LAGUNA MORENO SOFIA VALENTINA', 'F', 'V-11089456', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.00),
(34, 'LEON GUERRA SOFIA VALENTINA', 'F', 'V-33109561', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.00),
(36, 'Prueba', 'M', 'V-345764654', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seccion_b`
--

CREATE TABLE `seccion_b` (
  `Nro` int(9) NOT NULL,
  `Nombre_completo` varchar(100) NOT NULL,
  `Sexo` varchar(5) NOT NULL,
  `Cedula` varchar(50) NOT NULL,
  `Castellano` int(5) NOT NULL,
  `Matematica` int(5) NOT NULL,
  `GHC` int(5) NOT NULL,
  `Religion` int(5) NOT NULL,
  `Biologia` int(5) NOT NULL,
  `Computacion` int(5) NOT NULL,
  `Ingles` int(5) NOT NULL,
  `Arte` int(5) NOT NULL,
  `Educacion_fisica` int(5) NOT NULL,
  `Promedio` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `seccion_b`
--

INSERT INTO `seccion_b` (`Nro`, `Nombre_completo`, `Sexo`, `Cedula`, `Castellano`, `Matematica`, `GHC`, `Religion`, `Biologia`, `Computacion`, `Ingles`, `Arte`, `Educacion_fisica`, `Promedio`) VALUES
(1, 'BRICEÑO MONTIEL ROBINSON LUIS', 'M', 'V-13098098', 12, 17, 18, 19, 16, 17, 12, 13, 14, 15.33),
(2, 'CHANGANO RINCON ADRIANN ALEJANDRO', 'M', 'V-33455123', 14, 16, 18, 14, 13, 16, 16, 14, 14, 15.00),
(3, 'CHOURIO SOTO KEINER DANIEL', 'M', 'V-23937247', 13, 13, 15, 17, 17, 18, 19, 17, 14, 15.89),
(4, 'COLINA MILLAN ENMANUEL ANDRES', 'M', 'V-14987139', 12, 17, 17, 15, 14, 14, 15, 17, 17, 15.33),
(5, 'CUBILLAN CASTRO YULIANIS YULIETH', 'F', 'V-12095678', 12, 15, 17, 18, 15, 19, 15, 17, 19, 16.33),
(6, 'GIRADO BOHORQUEZ YEFRYD DE JESUS', 'M', 'V-11345876', 14, 15, 15, 17, 16, 18, 12, 16, 18, 15.67),
(7, 'JIMENEZ COLS ISABELLA LUCIA', 'F', 'V-1298421', 12, 11, 13, 17, 12, 12, 16, 16, 16, 13.89),
(8, 'LAMEDA ALVAREZ ANYIBEL VICTORIA ', 'F', 'V-11233455', 11, 11, 17, 18, 12, 11, 14, 19, 14, 14.11),
(9, 'LOBO PADRON YORMARY DE LOS ANGELES', 'F', 'V-7899880', 14, 11, 16, 19, 12, 13, 13, 15, 17, 14.44);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `segundo_lapso_a`
--

CREATE TABLE `segundo_lapso_a` (
  `Nro` int(5) NOT NULL,
  `Nombre_completo` varchar(100) NOT NULL,
  `Sexo` varchar(5) NOT NULL,
  `Cedula` varchar(50) NOT NULL,
  `Castellano` int(5) NOT NULL,
  `Matematica` int(5) NOT NULL,
  `GHC` int(5) NOT NULL,
  `Religion` int(5) NOT NULL,
  `Biologia` int(5) NOT NULL,
  `Computacion` int(5) NOT NULL,
  `Ingles` int(5) NOT NULL,
  `Arte` int(5) NOT NULL,
  `Educacion_fisica` int(5) NOT NULL,
  `Promedio` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `segundo_lapso_a`
--

INSERT INTO `segundo_lapso_a` (`Nro`, `Nombre_completo`, `Sexo`, `Cedula`, `Castellano`, `Matematica`, `GHC`, `Religion`, `Biologia`, `Computacion`, `Ingles`, `Arte`, `Educacion_fisica`, `Promedio`) VALUES
(1, 'AGELVIS LAREZ VICTORIA VALENTINA', 'F', 'V-33885411', 18, 18, 15, 19, 20, 20, 13, 4, 5, 14.67),
(2, 'AU GUTIERREZ YULEYDIS YANASKI', 'F', 'V-34987023', 12, 12, 11, 5, 7, 9, 10, 12, 14, 10.22),
(3, 'BERMUDEZ SULBARAN ALCIBETH JOVANNA', 'F', 'V-31701110', 12, 15, 17, 17, 11, 20, 19, 16, 10, 15.22),
(4, 'BRACHO BARRIOSNUEVO SANTIAGO JAVIER', 'M', 'V-34980190', 15, 16, 17, 18, 19, 20, 16, 17, 13, 16.78),
(5, 'CHACIN FERNANDEZ CAMILA VICTORIA', 'F', 'V-3467098', 14, 16, 18, 19, 12, 11, 10, 18, 20, 15.33),
(6, 'CHIRINOS CHOURIO JEIBER JOSE', 'M', 'V-23876149', 12, 13, 14, 20, 17, 18, 16, 10, 20, 15.56),
(7, 'GARCIA SANCHEZ RASHEILY PAOLA', 'F', 'V-10560190', 12, 11, 16, 17, 20, 18, 19, 13, 15, 15.67),
(32, 'GONZALEZ ACEVEDO SANTIAGO JAVIER ', 'M', 'V-12098145', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.00),
(33, 'LAGUNA MORENO SOFIA VALENTINA', 'F', 'V-11089456', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.00),
(34, 'LEON GUERRA SOFIA VALENTINA', 'F', 'V-33109561', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.00),
(36, 'Prueba', 'M', 'V-345764654', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `segundo_lapso_b`
--

CREATE TABLE `segundo_lapso_b` (
  `Nro` int(5) NOT NULL,
  `Nombre_completo` varchar(100) NOT NULL,
  `Sexo` varchar(5) NOT NULL,
  `Cedula` varchar(50) NOT NULL,
  `Castellano` int(5) NOT NULL,
  `Matematica` int(5) NOT NULL,
  `GHC` int(5) NOT NULL,
  `Religion` int(5) NOT NULL,
  `Biologia` int(5) NOT NULL,
  `Computacion` int(5) NOT NULL,
  `Ingles` int(5) NOT NULL,
  `Arte` int(5) NOT NULL,
  `Educacion_fisica` int(5) NOT NULL,
  `Promedio` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `segundo_lapso_b`
--

INSERT INTO `segundo_lapso_b` (`Nro`, `Nombre_completo`, `Sexo`, `Cedula`, `Castellano`, `Matematica`, `GHC`, `Religion`, `Biologia`, `Computacion`, `Ingles`, `Arte`, `Educacion_fisica`, `Promedio`) VALUES
(1, 'BRICEÑO MONTIEL ROBINSON LUIS', 'M', 'V-13098098', 12, 16, 18, 19, 12, 11, 10, 20, 20, 15.33),
(2, 'CHANGANO RINCON ADRIANN ALEJANDRO', 'M', 'V-33455123', 15, 17, 18, 12, 15, 17, 18, 20, 13, 16.11),
(3, 'CHOURIO SOTO KEINER DANIEL', 'M', 'V-23937247', 15, 12, 17, 18, 19, 19, 20, 11, 14, 16.11),
(4, 'COLINA MILLAN ENMANUEL ANDRES', 'M', 'V-14987139', 12, 20, 18, 12, 11, 12, 14, 15, 16, 14.44),
(5, 'CUBILLAN CASTRO YULIANIS YULIETH', 'F', 'V-12095678', 12, 11, 16, 17, 17, 16, 18, 19, 20, 16.22),
(6, 'GIRADO BOHORQUEZ YEFRYD DE JESUS', 'M', 'V-11345876', 13, 11, 12, 16, 17, 17, 11, 15, 20, 14.67),
(7, 'JIMENEZ COLS ISABELLA LUCIA', 'F', 'V-1298421', 12, 12, 16, 17, 17, 11, 18, 18, 17, 15.33),
(8, 'LAMEDA ALVAREZ ANYIBEL VICTORIA ', 'F', 'V-11233455', 4, 6, 16, 17, 3, 7, 8, 10, 20, 10.11),
(9, 'LOBO PADRON YORMARY DE LOS ANGELES', 'F', 'V-7899880', 13, 11, 14, 20, 3, 7, 5, 10, 20, 11.44);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tercer_lapso_a`
--

CREATE TABLE `tercer_lapso_a` (
  `Nro` int(5) NOT NULL,
  `Nombre_completo` varchar(100) NOT NULL,
  `Sexo` varchar(5) NOT NULL,
  `Cedula` varchar(50) NOT NULL,
  `Castellano` int(5) NOT NULL,
  `Matematica` int(5) NOT NULL,
  `GHC` int(5) NOT NULL,
  `Religion` int(5) NOT NULL,
  `Biologia` int(5) NOT NULL,
  `Computacion` int(5) NOT NULL,
  `Ingles` int(5) NOT NULL,
  `Arte` int(5) NOT NULL,
  `Educacion_fisica` int(5) NOT NULL,
  `Promedio` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tercer_lapso_a`
--

INSERT INTO `tercer_lapso_a` (`Nro`, `Nombre_completo`, `Sexo`, `Cedula`, `Castellano`, `Matematica`, `GHC`, `Religion`, `Biologia`, `Computacion`, `Ingles`, `Arte`, `Educacion_fisica`, `Promedio`) VALUES
(1, 'AGELVIS LAREZ VICTORIA VALENTINA', 'F', 'V-33885411', 15, 17, 18, 11, 12, 10, 14, 12, 15, 13.78),
(2, 'AU GUTIERREZ YULEYDIS YANASKI', 'F', 'V-34987023', 11, 17, 16, 16, 14, 4, 7, 3, 12, 11.11),
(3, 'BERMUDEZ SULBARAN ALCIBETH JOVANNA', 'F', 'V-31701110', 13, 12, 11, 10, 20, 19, 20, 18, 15, 15.33),
(4, 'BRACHO BARRIOSNUEVO SANTIAGO JAVIER', 'M', 'V-34980190', 14, 17, 11, 18, 3, 7, 12, 20, 12, 12.67),
(5, 'CHACIN FERNANDEZ CAMILA VICTORIA', 'F', 'V-3467098', 15, 18, 11, 19, 18, 11, 5, 6, 15, 13.11),
(6, 'CHIRINOS CHOURIO JEIBER JOSE', 'M', 'V-23876149', 12, 5, 7, 12, 17, 16, 18, 20, 13, 13.33),
(7, 'GARCIA SANCHEZ RASHEILY PAOLA', 'F', 'V-10560190', 11, 14, 13, 16, 16, 7, 16, 17, 15, 13.89),
(32, 'GONZALEZ ACEVEDO SANTIAGO JAVIER ', 'M', 'V-12098145', 15, 16, 18, 13, 20, 17, 18, 11, 13, 15.67),
(33, 'LAGUNA MORENO SOFIA VALENTINA', 'F', 'V-11089456', 14, 16, 20, 17, 15, 17, 18, 12, 11, 15.56),
(34, 'LEON GUERRA SOFIA VALENTINA', 'F', 'V-33109561', 13, 15, 16, 18, 13, 20, 16, 11, 14, 15.11),
(36, 'Prueba', 'M', 'V-345764654', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tercer_lapso_b`
--

CREATE TABLE `tercer_lapso_b` (
  `Nro` int(5) NOT NULL,
  `Nombre_completo` varchar(100) NOT NULL,
  `Sexo` varchar(5) NOT NULL,
  `Cedula` varchar(50) NOT NULL,
  `Castellano` int(5) NOT NULL,
  `Matematica` int(5) NOT NULL,
  `GHC` int(5) NOT NULL,
  `Religion` int(5) NOT NULL,
  `Biologia` int(5) NOT NULL,
  `Computacion` int(5) NOT NULL,
  `Ingles` int(5) NOT NULL,
  `Arte` int(5) NOT NULL,
  `Educacion_fisica` int(5) NOT NULL,
  `Promedio` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tercer_lapso_b`
--

INSERT INTO `tercer_lapso_b` (`Nro`, `Nombre_completo`, `Sexo`, `Cedula`, `Castellano`, `Matematica`, `GHC`, `Religion`, `Biologia`, `Computacion`, `Ingles`, `Arte`, `Educacion_fisica`, `Promedio`) VALUES
(1, 'BRICEÑO MONTIEL ROBINSON LUIS', 'M', 'V-13098098', 12, 15, 17, 18, 17, 19, 12, 13, 20, 15.89),
(2, 'CHANGANO RINCON ADRIANN ALEJANDRO', 'M', 'V-33455123', 15, 18, 19, 14, 12, 12, 16, 18, 19, 15.89),
(3, 'CHOURIO SOTO KEINER DANIEL', 'M', 'V-23937247', 11, 15, 17, 18, 14, 17, 18, 20, 15, 16.11),
(4, 'COLINA MILLAN ENMANUEL ANDRES', 'M', 'V-14987139', 12, 16, 18, 19, 20, 11, 16, 17, 15, 16.00),
(5, 'CUBILLAN CASTRO YULIANIS YULIETH', 'F', 'V-12095678', 12, 16, 17, 18, 19, 20, 11, 14, 16, 15.89),
(6, 'GIRADO BOHORQUEZ YEFRYD DE JESUS', 'M', 'V-11345876', 14, 18, 16, 16, 11, 17, 12, 20, 15, 15.44),
(7, 'JIMENEZ COLS ISABELLA LUCIA', 'F', 'V-1298421', 15, 12, 11, 16, 6, 9, 13, 10, 13, 11.67),
(8, 'LAMEDA ALVAREZ ANYIBEL VICTORIA ', 'F', 'V-11233455', 12, 11, 17, 18, 20, 12, 17, 18, 11, 15.11),
(9, 'LOBO PADRON YORMARY DE LOS ANGELES', 'F', 'V-7899880', 13, 3, 16, 18, 20, 15, 17, 19, 20, 15.67);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administradores`
--
ALTER TABLE `administradores`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `primer_lapso_a`
--
ALTER TABLE `primer_lapso_a`
  ADD PRIMARY KEY (`Nro`);

--
-- Indices de la tabla `primer_lapso_b`
--
ALTER TABLE `primer_lapso_b`
  ADD PRIMARY KEY (`Nro`);

--
-- Indices de la tabla `registro_estudiantes_a`
--
ALTER TABLE `registro_estudiantes_a`
  ADD PRIMARY KEY (`Nro`);

--
-- Indices de la tabla `registro_estudiantes_b`
--
ALTER TABLE `registro_estudiantes_b`
  ADD PRIMARY KEY (`Nro`);

--
-- Indices de la tabla `seccion_a`
--
ALTER TABLE `seccion_a`
  ADD PRIMARY KEY (`Nro`);

--
-- Indices de la tabla `seccion_b`
--
ALTER TABLE `seccion_b`
  ADD PRIMARY KEY (`Nro`);

--
-- Indices de la tabla `segundo_lapso_a`
--
ALTER TABLE `segundo_lapso_a`
  ADD PRIMARY KEY (`Nro`);

--
-- Indices de la tabla `segundo_lapso_b`
--
ALTER TABLE `segundo_lapso_b`
  ADD PRIMARY KEY (`Nro`);

--
-- Indices de la tabla `tercer_lapso_a`
--
ALTER TABLE `tercer_lapso_a`
  ADD PRIMARY KEY (`Nro`);

--
-- Indices de la tabla `tercer_lapso_b`
--
ALTER TABLE `tercer_lapso_b`
  ADD PRIMARY KEY (`Nro`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administradores`
--
ALTER TABLE `administradores`
  MODIFY `ID` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `primer_lapso_a`
--
ALTER TABLE `primer_lapso_a`
  MODIFY `Nro` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT de la tabla `primer_lapso_b`
--
ALTER TABLE `primer_lapso_b`
  MODIFY `Nro` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `registro_estudiantes_a`
--
ALTER TABLE `registro_estudiantes_a`
  MODIFY `Nro` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT de la tabla `registro_estudiantes_b`
--
ALTER TABLE `registro_estudiantes_b`
  MODIFY `Nro` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `seccion_a`
--
ALTER TABLE `seccion_a`
  MODIFY `Nro` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT de la tabla `seccion_b`
--
ALTER TABLE `seccion_b`
  MODIFY `Nro` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `segundo_lapso_a`
--
ALTER TABLE `segundo_lapso_a`
  MODIFY `Nro` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT de la tabla `segundo_lapso_b`
--
ALTER TABLE `segundo_lapso_b`
  MODIFY `Nro` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `tercer_lapso_a`
--
ALTER TABLE `tercer_lapso_a`
  MODIFY `Nro` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT de la tabla `tercer_lapso_b`
--
ALTER TABLE `tercer_lapso_b`
  MODIFY `Nro` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
