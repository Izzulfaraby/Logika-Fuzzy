-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 20, 2026 at 10:37 AM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_fuzzy_usia`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_domain_usia_anak`
--

DROP TABLE IF EXISTS `tb_domain_usia_anak`;
CREATE TABLE IF NOT EXISTS `tb_domain_usia_anak` (
  `id` int NOT NULL AUTO_INCREMENT,
  `b_bawah` int NOT NULL,
  `b_atas` int NOT NULL,
  `fungsi` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tb_domain_usia_anak`
--

INSERT INTO `tb_domain_usia_anak` (`id`, `b_bawah`, `b_atas`, `fungsi`) VALUES
(1, 0, 6, '0'),
(2, 6, 8, 'trapezium_up'),
(3, 8, 9, '1'),
(4, 9, 11, 'trapezium_down'),
(5, 11, 150, '0');

-- --------------------------------------------------------

--
-- Table structure for table `tb_domain_usia_bayi`
--

DROP TABLE IF EXISTS `tb_domain_usia_bayi`;
CREATE TABLE IF NOT EXISTS `tb_domain_usia_bayi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `b_bawah` int NOT NULL,
  `b_atas` int NOT NULL,
  `fungsi` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tb_domain_usia_bayi`
--

INSERT INTO `tb_domain_usia_bayi` (`id`, `b_bawah`, `b_atas`, `fungsi`) VALUES
(1, 0, 2, '1'),
(2, 2, 5, 'trapezium_down'),
(3, 5, 150, '0');

-- --------------------------------------------------------

--
-- Table structure for table `tb_domain_usia_dewasa`
--

DROP TABLE IF EXISTS `tb_domain_usia_dewasa`;
CREATE TABLE IF NOT EXISTS `tb_domain_usia_dewasa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `b_bawah` int NOT NULL,
  `b_atas` int NOT NULL,
  `fungsi` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tb_domain_usia_dewasa`
--

INSERT INTO `tb_domain_usia_dewasa` (`id`, `b_bawah`, `b_atas`, `fungsi`) VALUES
(1, 0, 20, '0'),
(2, 20, 22, 'trapezium_up'),
(3, 22, 63, '1'),
(4, 63, 65, 'trapezium_down'),
(5, 65, 150, '0');

-- --------------------------------------------------------

--
-- Table structure for table `tb_domain_usia_lansia`
--

DROP TABLE IF EXISTS `tb_domain_usia_lansia`;
CREATE TABLE IF NOT EXISTS `tb_domain_usia_lansia` (
  `id` int NOT NULL AUTO_INCREMENT,
  `b_bawah` int NOT NULL,
  `b_atas` int NOT NULL,
  `fungsi` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tb_domain_usia_lansia`
--

INSERT INTO `tb_domain_usia_lansia` (`id`, `b_bawah`, `b_atas`, `fungsi`) VALUES
(1, 0, 65, '0'),
(2, 65, 70, 'trapezium_up'),
(3, 70, 95, '1'),
(4, 95, 100, 'trapezium_down'),
(5, 100, 150, '0');

-- --------------------------------------------------------

--
-- Table structure for table `tb_domain_usia_pemuda`
--

DROP TABLE IF EXISTS `tb_domain_usia_pemuda`;
CREATE TABLE IF NOT EXISTS `tb_domain_usia_pemuda` (
  `id` int NOT NULL AUTO_INCREMENT,
  `b_bawah` int NOT NULL,
  `b_atas` int NOT NULL,
  `fungsi` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tb_domain_usia_pemuda`
--

INSERT INTO `tb_domain_usia_pemuda` (`id`, `b_bawah`, `b_atas`, `fungsi`) VALUES
(1, 0, 15, '0'),
(2, 15, 17, 'trapezium_up'),
(3, 17, 22, '1'),
(4, 22, 24, 'trapezium_down'),
(5, 24, 150, '0');

-- --------------------------------------------------------

--
-- Table structure for table `tb_domain_usia_remaja`
--

DROP TABLE IF EXISTS `tb_domain_usia_remaja`;
CREATE TABLE IF NOT EXISTS `tb_domain_usia_remaja` (
  `id` int NOT NULL AUTO_INCREMENT,
  `b_bawah` int NOT NULL,
  `b_atas` int NOT NULL,
  `fungsi` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tb_domain_usia_remaja`
--

INSERT INTO `tb_domain_usia_remaja` (`id`, `b_bawah`, `b_atas`, `fungsi`) VALUES
(1, 0, 10, '0'),
(2, 10, 12, 'trapezium_up'),
(3, 12, 17, '1'),
(4, 17, 19, 'trapezium_down'),
(5, 19, 150, '0');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
