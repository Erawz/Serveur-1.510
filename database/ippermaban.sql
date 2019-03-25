-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le :  jeu. 14 mars 2019 à 20:24
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
-- Structure de la table `ippermaban`
--

CREATE TABLE `ippermaban` (
  `ip` longtext NOT NULL,
  `bannedby` longtext NOT NULL,
  `reason` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Déchargement des données de la table `ippermaban`
--

INSERT INTO `ippermaban` (`ip`, `bannedby`, `reason`) VALUES
('78.185.114.133', 'Duxo', 'GG'),
('50.3.86.135', 'Duxo', 'Gelmeye DEVAM ETME GG OLACAN KOCUM YA'),
('5.2.64.162', 'Duxo', 'GG OlmuÅŸen uÅŸak'),
('185.65.206.148', 'Duxo', 'TRYÄ°NG MORUG'),
('178.243.3.116', 'Duxo', 'Selametin HayrÄ± Olsun'),
('78.190.152.11', 'Duxo', ''),
('95.8.38.149', 'Duxo', 'Teyzende'),
('85.97.112.108', 'Duxo', ''),
('85.104.167.33', 'Dexter', 'iÅŸine gg'),
('85.104.167.33', 'Seqquh', 'GGLENDÄ°N'),
('88.230.129.238', 'Duxo', ''),
('101.127.206.221', 'Dexter', 'atÄ±nca annenle bana haber ver'),
('46.2.117.113', 'Dexter', 'sg'),
('46.196.197.132', 'Duxo', ''),
('176.234.212.117', 'Duxo', 'Ä°lettim'),
('85.98.205.92', 'Duxo', 'Bi BÄ°tmiyorsunuz APtal Oruspu cocuklarÄ±'),
('178.62.29.27', 'Duxo', 'GG'),
('88.244.178.78', 'Duxo', ''),
('78.160.154.181', 'Duxo', 'Pardon yanlÄ±ÅŸlÄ±kla oldu'),
('207.244.113.36', 'Dexter', 'Advertisement'),
('46.196.197.132', 'Duxo', 'Ã‡Ã¶p SWNÄ°Z'),
('178.243.56.170', 'Duxo', 'Advertisement'),
('88.253.33.184', 'Duxo', ''),
('207.244.113.36', 'Duxo', ''),
('85.98.50.139', 'Hke', ''),
('78.171.232.252', 'Dolunay', 'hadi git serverine tabi aÃ§Ä±ksa'),
('88.230.87.131', 'Dolunay', 'serverine git'),
('95.8.13.228', 'Duxo', 'Ä°yi geceler krdÅŸm'),
('5.47.148.35', 'Dexter', ''),
('88.254.86.182', 'Sunset', 'SATICI'),
('78.174.213.123', 'Duxo', ''),
('176.234.215.230', 'Duxo', ''),
('31.14.75.48', 'Duxo', 'Annen Var'),
('46.196.197.132', 'Duxo', 'BB'),
('88.228.159.51', 'Duxo', ''),
('207.244.113.44', 'Dexter', 'anti Vpn'),
('107.178.36.26', 'Dexter', 'Selsium'),
('46.196.197.132', 'Dexter', ''),
('85.104.161.242', 'Duxo', ''),
('78.191.165.137', 'Duxo', 'Sormuorum'),
('88.246.164.209', 'Dexter', 'bb o zaman'),
('88.232.174.56', 'Duxo', ''),
('78.170.174.14', 'Duxo', 'Bende senin'),
('88.246.143.87', 'Duxo', ''),
('78.161.53.12', 'Duxo', ''),
('185.90.61.163', 'Brahmeerich', 'Peki'),
('185.90.61.52', 'Brahmeerich', ''),
('45.33.139.217', 'Brahmeerich', ''),
('46.196.197.132', 'Nates', 'Siktir git'),
('178.255.43.149', 'Duxo', ''),
('31.14.75.67', 'Duxo', ''),
('88.224.40.206', 'Jeanlaus', 'Reklam'),
('46.196.197.132', 'Nates', 'ModeratÃ¶r olduÄŸunu hiÃ§ bir zaman unutma. GÃ¼le gÃ¼le'),
('46.196.197.132', 'Nates', ''),
('88.254.203.129', 'Eurene', 'sg'),
('46.196.197.132', 'Rozes', ''),
('78.185.59.245', 'Eurene', 'ANANI'),
('31.14.75.57', 'Eurene', 'Sikirin.simdi'),
('78.171.130.57', 'Krone', 'bb'),
('78.171.130.57', 'Krone', 'bb'),
('88.226.229.238', 'Killarus', 'anana hÃ¼kmederm'),
('88.226.229.238', 'Killarus', 'anana hÃ¼kmederm'),
('177.47.27.229', 'Laudatory', 'adv'),
('177.47.27.229', 'Laudatory', 'adv'),
('78.190.159.20', 'Krone', 'seni dÃ¶lÃ¼mde boÄŸarÄ±m'),
('78.190.159.20', 'Krone', 'seni dÃ¶lÃ¼mde boÄŸarÄ±m'),
('85.108.138.124', 'Gifted', 'ÅŸansÄ±nÄ± ii kullanmalÄ±ydÄ±n'),
('85.108.138.124', 'Gifted', 'ÅŸansÄ±nÄ± ii kullanmalÄ±ydÄ±n'),
('78.179.92.134', 'Gifted#8888', 'Batunun YanÄ±na git krdÅŸm.'),
('78.179.92.134', 'Gifted#8888', 'Batunun YanÄ±na git krdÅŸm.'),
('95.14.65.4', 'Gifted#8888', 'Bende sokmuorm ozmn'),
('95.14.65.4', 'Gifted#8888', 'Bende sokmuorm ozmn'),
('95.8.210.241', 'Satanistic', 'SG LAN'),
('95.8.210.241', 'Satanistic', 'SG LAN'),
('85.108.175.50', 'Satanistic', 'ASLANIM SENÄ°N ADAM OL DEMENLE OLMADIK KÄ° OROSBU OL DEMEKLE OLALIM'),
('85.108.175.50', 'Satanistic', 'ASLANIM SENÄ°N ADAM OL DEMENLE OLMADIK KÄ° OROSBU OL DEMEKLE OLALIM');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
