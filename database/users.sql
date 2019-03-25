-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le :  sam. 09 mars 2019 à 10:18
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
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `Username` longtext NOT NULL,
  `Password` longtext NOT NULL,
  `PlayerID` int(11) NOT NULL,
  `PrivLevel` int(11) NOT NULL,
  `TitleNumber` int(11) NOT NULL,
  `FirstCount` int(11) NOT NULL,
  `CheeseCount` int(11) NOT NULL,
  `ShamanCheeses` int(11) NOT NULL,
  `ShopCheeses` int(11) NOT NULL,
  `ShopFraises` int(11) NOT NULL,
  `ShamanSaves` int(11) NOT NULL,
  `HardModeSaves` int(11) NOT NULL,
  `DivineModeSaves` int(11) NOT NULL,
  `BootcampCount` int(11) NOT NULL,
  `ShamanType` int(11) NOT NULL,
  `ShopItems` longtext NOT NULL,
  `ShamanItems` longtext NOT NULL,
  `Clothes` longtext NOT NULL,
  `Look` longtext NOT NULL,
  `ShamanLook` longtext NOT NULL,
  `MouseColor` longtext NOT NULL,
  `ShamanColor` longtext NOT NULL,
  `RegDate` int(11) NOT NULL,
  `Badges` longtext NOT NULL,
  `CheeseTitleList` longtext NOT NULL,
  `FirstTitleList` longtext NOT NULL,
  `ShamanTitleList` longtext NOT NULL,
  `ShopTitleList` longtext NOT NULL,
  `BootcampTitleList` longtext NOT NULL,
  `HardModeTitleList` longtext NOT NULL,
  `DivineModeTitleList` longtext NOT NULL,
  `SpecialTitleList` longtext NOT NULL,
  `BanHours` int(11) NOT NULL,
  `ShamanLevel` int(11) NOT NULL,
  `ShamanExp` int(11) NOT NULL,
  `ShamanExpNext` int(11) NOT NULL,
  `Skills` longtext NOT NULL,
  `LastOn` int(11) NOT NULL,
  `FriendsList` longtext NOT NULL,
  `IgnoredsList` longtext NOT NULL,
  `Gender` int(11) NOT NULL,
  `LastDivorceTimer` int(11) NOT NULL,
  `Marriage` longtext NOT NULL,
  `TribeCode` int(11) NOT NULL,
  `TribeRank` int(11) NOT NULL,
  `TribeJoined` int(11) NOT NULL,
  `Gifts` longtext NOT NULL,
  `Messages` longtext NOT NULL,
  `SurvivorStats` longtext NOT NULL,
  `RacingStats` longtext NOT NULL,
  `Consumables` longtext NOT NULL,
  `EquipedConsumables` longtext NOT NULL,
  `Pet` int(11) NOT NULL,
  `PetEnd` int(11) NOT NULL,
  `ShamanBadges` longtext NOT NULL,
  `EquipedShamanBadge` int(11) NOT NULL,
  `UnRanked` int(11) NOT NULL,
  `totemitemcount` int(11) NOT NULL,
  `totem` longtext NOT NULL,
  `VisuDone` longtext NOT NULL,
  `customitems` longtext NOT NULL,
  `coins` int(11) NOT NULL,
  `tokens` int(11) NOT NULL,
  `deathstats` longtext NOT NULL,
  `viptime` int(11) NOT NULL,
  `langue` longtext NOT NULL,
  `mayor` longtext NOT NULL,
  `notificationcode` longtext NOT NULL,
  `VipInfos` longtext NOT NULL,
  `aventurecounts` longtext NOT NULL,
  `aventurepoints` longtext NOT NULL,
  `savesaventure` int(11) NOT NULL,
  `user_community` varchar(3) NOT NULL DEFAULT 'xx',
  `avatar` varchar(30) NOT NULL DEFAULT '0.jpg',
  `user_line_status` int(1) NOT NULL DEFAULT '1',
  `user_token` text NOT NULL,
  `user_email` varchar(70) NOT NULL DEFAULT '0',
  `user_birthday` varchar(20) NOT NULL DEFAULT '0',
  `user_location` varchar(50) NOT NULL DEFAULT '0',
  `user_presentation` text NOT NULL,
  `user_sanction_status` varchar(10) NOT NULL DEFAULT '0',
  `user_line_param` int(11) NOT NULL DEFAULT '1',
  `Email` longtext NOT NULL,
  `DailyQuest` longtext NOT NULL,
  `RemainingMissions` int(11) NOT NULL,
  `Letters` longtext NOT NULL,
  `recCount` int(11) NOT NULL,
  `deathCount` int(11) NOT NULL,
  `user_title_forum` text NOT NULL,
  `Time` int(11) NOT NULL,
  `Karma` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`Username`, `Password`, `PlayerID`, `PrivLevel`, `TitleNumber`, `FirstCount`, `CheeseCount`, `ShamanCheeses`, `ShopCheeses`, `ShopFraises`, `ShamanSaves`, `HardModeSaves`, `DivineModeSaves`, `BootcampCount`, `ShamanType`, `ShopItems`, `ShamanItems`, `Clothes`, `Look`, `ShamanLook`, `MouseColor`, `ShamanColor`, `RegDate`, `Badges`, `CheeseTitleList`, `FirstTitleList`, `ShamanTitleList`, `ShopTitleList`, `BootcampTitleList`, `HardModeTitleList`, `DivineModeTitleList`, `SpecialTitleList`, `BanHours`, `ShamanLevel`, `ShamanExp`, `ShamanExpNext`, `Skills`, `LastOn`, `FriendsList`, `IgnoredsList`, `Gender`, `LastDivorceTimer`, `Marriage`, `TribeCode`, `TribeRank`, `TribeJoined`, `Gifts`, `Messages`, `SurvivorStats`, `RacingStats`, `Consumables`, `EquipedConsumables`, `Pet`, `PetEnd`, `ShamanBadges`, `EquipedShamanBadge`, `UnRanked`, `totemitemcount`, `totem`, `VisuDone`, `customitems`, `coins`, `tokens`, `deathstats`, `viptime`, `langue`, `mayor`, `notificationcode`, `VipInfos`, `aventurecounts`, `aventurepoints`, `savesaventure`, `user_community`, `avatar`, `user_line_status`, `user_token`, `user_email`, `user_birthday`, `user_location`, `user_presentation`, `user_sanction_status`, `user_line_param`, `Email`, `DailyQuest`, `RemainingMissions`, `Letters`, `recCount`, `deathCount`, `user_title_forum`, `Time`, `Karma`) VALUES
('Gifted', 'k/WHDZD9oxJf/nxooBKphDp1esOnRfd+jacgYig2iic=', 107, 15, 0, 0, 20, 0, 1998520, 999000, 4, 0, 0, 0, 0, '230121,230122,809', '', '', '122;0,0,0,0,0,0,0,0,9,0,0', '0,0,0,0,0,0,0,0,0,0', '78583a', '95d9d6', 1550067747, '{\'229\': 0, \'228\': 0}', '', '', '', '115.1,116.1', '', '', '', '', 0, 100, 0, 100, '', 25837251, 'Derya', '', 2, 0, '', 217, 8, 25836267, '', '', '13,3,5,2', '36,0,0,0', '35:198;2236:200;2267:200;23:9', '', 0, 1550235091, '', 0, 0, 0, '', '', '', 0, 0, '2,8,0,0,0,189,133,0,0', 0, 'TR', '0#0#0#0#0#0', '', '', '', '24:0', 0, 'xx', '107/107.jpg', 2, '21db7d4a31547e76399aa24c2480dd95', '0', '0', '0', '', '0', 1, 'Sksk@gmail.com', '2,0,4,1', 3, '', 0, 0, 'MiceFun Mouse', 0, 0),
('Loveditoi', '4uQ6DJsd+ulaMY2AUwJ0yj6N1Hj4qnuWE4R6Q3VPqAg=', 461, 15, 0, 0, 0, 0, 1999500, 1000000, 0, 0, 0, 0, 0, '', '', '', '1;0,0,0,0,0,0,0,0,0,0,0', '0,0,0,0,0,0,0,0,0,0', '78583a', '95d9d6', 1552122913, '{}', '', '', '', '', '', '', '', '', 0, 300, 0, 100, '', 25868717, '', '', 0, 0, '', 219, 9, 25868717, '', '', '0,0,0,0', '0,0,0,0', '2256:5;2379:5;2252:5;2349:5;23:10', '', 0, 1552123066, '', 0, 0, 0, '', '', '', 0, 0, '2,8,0,0,0,189,133,0,0', 0, 'FR', '0#0#0#0#0#0', '', '', '', '24:0', 0, 'xx', '0.jpg', 1, '', '0', '0', '0', '', '0', 1, 'bestmicere@gmail.com', '6,2,5,0', 4, '', 0, 0, 'Little Mouse', 153, 0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
