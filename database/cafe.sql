-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 22 Oca 2019, 12:29:22
-- Sunucu sürümü: 10.1.37-MariaDB
-- PHP Sürümü: 7.3.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `cafe`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `cafeposts`
--

CREATE TABLE `cafeposts` (
  `PostID` int(11) NOT NULL,
  `TopicID` int(11) NOT NULL,
  `Name` longtext CHARACTER SET utf8 NOT NULL,
  `Post` longtext CHARACTER SET utf8 NOT NULL,
  `Date` int(11) NOT NULL,
  `Points` int(11) NOT NULL,
  `Votes` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `cafetopics`
--

CREATE TABLE `cafetopics` (
  `TopicID` int(11) NOT NULL,
  `Title` longtext CHARACTER SET utf8 NOT NULL,
  `Author` longtext CHARACTER SET utf8 NOT NULL,
  `LastPostName` longtext CHARACTER SET utf8 NOT NULL,
  `Posts` int(11) NOT NULL,
  `Date` int(11) NOT NULL,
  `Langue` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
