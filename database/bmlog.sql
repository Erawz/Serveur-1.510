-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le :  jeu. 14 mars 2019 à 20:21
-- Version du serveur :  10.1.38-MariaDB
-- Version de PHP :  7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `transformice 1.510`
--

-- --------------------------------------------------------

--
-- Structure de la table `bmlog`
--

CREATE TABLE `bmlog` (
  `Name` text NOT NULL,
  `State` text NOT NULL,
  `Timestamp` text NOT NULL,
  `Bannedby` text NOT NULL,
  `Time` text NOT NULL,
  `Reason` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Déchargement des données de la table `bmlog`
--

INSERT INTO `bmlog` (`Name`, `State`, `Timestamp`, `Bannedby`, `Time`, `Reason`) VALUES
('Himan', 'MUTE', '1550068011', 'Gifted', '1', ''),
('Himan', 'MUTE', '1550068018', 'Gifted', '0', 'sorry xd'),
('Satanistic', 'MUTE', '1550069955', 'Gifted', '0', 'test'),
('Noob147', 'MUTE', '1550074891', 'Whitesound', '1', 'test'),
('Noob147', 'BAN', '1550075170', 'Gifted', '0', ''),
('Test', 'MUTE', '1550075568', 'Test', '0', '.'),
('Himan', 'BAN', '1550084070', 'Fl4sh_c', '1', ''),
('Napolyy', 'MUTE', '1551205634', 'Napolyy', '1', 'test'),
('Napolyy', 'MUTE', '1551205663', 'Napolyy', '0', ''),
('Batua', 'MUTE', '1551215298', 'Batu', '1', 'deneme'),
('Batua', 'MUTE', '1551215362', 'Batu', '1', ''),
('Batua', 'MUTE', '1551215370', 'Batu', '1', ''),
('Batua', 'MUTE', '1551215410', 'Batu', '1', ''),
('Batua', 'MUTE', '1551215427', 'Batu', '0', ''),
('Batua', 'MUTE', '1551215451', 'Batu', '0', ''),
('Batua', 'MUTE', '1551216845', 'Batu', '0', 'deneme');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
