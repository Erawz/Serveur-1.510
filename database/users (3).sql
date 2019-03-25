-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le :  jeu. 14 mars 2019 à 20:28
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
('Loveditoi', '4uQ6DJsd+ulaMY2AUwJ0yj6N1Hj4qnuWE4R6Q3VPqAg=', 461, 11, 447, 98745, 188745, 87584, 1990800, 999980, 387489, 198326, 178584, 87458, 0, '230119,41_FFF8F2,201_00FFFF', '', '', '119;41_FFF8F2,0,1_00FFFF,0,0,0,0,0,0,0,0', '0,0,0,0,0,0,0,0,0,0', '39FFF4', '95d9d6', 1552122913, '{\'226\': 0}', '5.1,6.1,7.1,8.1,35.1,36.1,37.1,26.1,27.1,28.1,29.1,30.1,31.1,32.1,33.1,34.1,38.1,39.1,40.1,41.1,72.1,73.1,74.1,75.1,76.1,77.1,78.1,79.1,80.1,81.1,82.1,83.1,84.1,85.1,86.1,87.1,88.1,89.1,90.1,91.1,92.1,234.1,235.1,236.1,237.1,238.1,93.1', '9.1,10.1,11.1,12.1,42.1,43.1,44.1,45.1,46.1,47.1,48.1,49.1,50.1,51.1,52.1,53.1,54.1,55.1,56.1,57.1,58.1,59.1,60.1,61.1,62.1,63.1,64.1,65.1,66.1,67.1,68.1,69.1,231.1,232.1,233.1,70.1,224.1,225.1,226.1,227.1,202.1,228.1,229.1,230.1,71.1', '1.1,2.1,3.1,4.1,13.1,14.1,15.1,16.1,17.1,18.1,19.1,20.1,21.1,22.1,23.1,24.1,25.1,94.1,95.1,96.1,97.1,98.1,99.1,100.1,101.1,102.1,103.1,104.1,105.1,106.1,107.1,108.1,109.1,110.1,111.1,112.1,113.1,114.1,115.1', '115.1,116.1', '256.9,257.9,258.9,259.9,260.9,261.9,262.9,263.9,264.9,265.9,266.9,267.9,268.9,269.9,270.9,271.9,272.9,273.9,274.9,275.9,276.9,277.9,278.9,279.9,280.9,281.9,282.9,283.9,284.9,285.9,286.9', '213.1,214.1,215.1,216.1,217.1,218.1,219.1,220.1,221.1,222.1,223.1', '324.1,325.1,326.1,327.1,328.1,329.1,330.1,331.1,332.1,333.1,334.1', '', 0, 300, 0, 100, '0:5;1:5;2:5;3:5;4:1;5:5;6:5;7:1;8:5;9:5;10:1;11:5;12:5;13:1;14:1;20:5;21:5;22:5;23:5;24:1;25:5;26:5;27:1;28:5;29:5;30:1;31:5;32:5;33:1;34:1;40:5;41:5;42:5;43:5;44:1;45:5;46:5;47:1;48:5;49:5;50:1;51:5;52:5;53:1;54:1;60:5;61:5;62:5;63:5;64:1;65:5;66:5;67:1;68:5;69:5;70:1;71:5;72:5;73:1;74:5;80:5;82:5;83:5;84:1;85:5;86:5;87:1;88:5;89:5;90:1;91:1;92:1;93:5;94:1', 25876519, '', '', 1, 0, '', 219, 9, 25868717, '', '', '0,0,0,0', '0,0,0,0', '2256:5;2379:5;2252:5;2349:5;23:10', '', 0, 1552591161, '', 0, 0, 0, '', '', '41,201', 0, 0, '2,8,0,0,0,189,133,0,0', 0, 'FR', '0#0#0#0#0#0', '', '', '', '24:0', 0, 'xx', '0.jpg', 1, '', '0', '0', '0', '', '0', 1, 'bestmicere@gmail.com', '6,2,5,0', 4, '', 0, 0, 'Little Mouse', 3966, 0),
('Lueker', '4uQ6DJsd+ulaMY2AUwJ0yj6N1Hj4qnuWE4R6Q3VPqAg=', 462, 11, 0, 10000, 15000, 5000, 20000, 10000, 20000, 10000, 10000, 5000, 0, '', '', '', '1;0,0,0,0,0,0,0,0,0,0,0', '0,0,0,0,0,0,0,0,0,0', '78583a', '95d9d6', 1552127209, '{1: 1}', '5.1,6.1,7.1,8.1,35.1,36.1,37.1,26.1,27.1,28.1,29.1,30.1,31.1,32.1,33.1,34.1,38.1,39.1,40.1,41.1,72.1,73.1,74.1,75.1,76.1,77.1,78.1,79.1,80.1,81.1,82.1,83.1,84.1,85.1,86.1,87.1,88.1,89.1,90.1,91.1,92.1,234.1,235.1,236.1,237.1,238.1,93.1', '9.1,10.1,11.1,12.1,42.1,43.1,44.1,45.1,46.1,47.1,48.1,49.1,50.1,51.1,52.1,53.1,54.1,55.1,56.1,57.1,58.1,59.1,60.1,61.1,62.1,63.1,64.1,65.1,66.1,67.1,68.1,69.1,231.1,232.1,233.1', '1.1,2.1,3.1,4.1,13.1,14.1,15.1,16.1,17.1,18.1,19.1,20.1,21.1,22.1,23.1,24.1,25.1,94.1,95.1,96.1', '', '256.5,257.5,258.5,259.5,260.5,261.5,262.5,263.5,264.5,265.5,266.5,267.5,268.5,269.5,270.5,271.5,272.5,273.5,274.5,275.5,276.5,277.5,278.5,279.5,280.5,281.5,282.5,283.5,284.5,285.5,286.5', '213.1,214.1,215.1,216.1,217.1', '324.1,325.1,326.1,327.1,328.1', '', 0, 300, 0, 100, '0:5;1:5;2:5;3:5;4:1;5:5;6:5;7:1;8:5;9:5;10:1;11:5;12:5;13:1;14:1;20:5;21:5;22:5;23:5;24:1;25:5;26:5;27:1;28:5;29:5;30:1;31:5;32:5;33:1;34:1;40:5;41:5;42:5;43:5;44:1;45:5;46:5;47:1;48:5;49:5;50:1;51:5;52:5;53:1;54:1;60:5;61:5;62:5;63:5;64:1;65:5;66:5;67:1;68:5;69:5;70:1;71:5;72:5;73:1;74:5;80:5;82:5;83:5;84:1;85:5;86:5;87:1;88:5;89:5;90:1;91:1;92:1;93:5;94:1', 25868853, '', '', 2, 0, '', 219, 8, 25868794, '', '', '0,0,0,0', '0,0,0,0', '2256:5;2379:5;2252:5;2349:5;23:10', '', 0, 1552131222, '', 0, 0, 0, '', '', '', 0, 0, '2,8,0,0,0,189,133,0,0', 0, 'FR', '0#0#0#0#0#0', '', '', '', '24:0', 0, 'xx', '0.jpg', 1, '', '0', '0', '0', '', '0', 1, 'rodriguez.maxence@yahoo.fr', '5,3,6,1', 4, '', 0, 0, 'Little Mouse', 1263, 0),
('Test', '4uQ6DJsd+ulaMY2AUwJ0yj6N1Hj4qnuWE4R6Q3VPqAg=', 462, 1, 0, 10000, 15000, 5000, 20000, 10000, 20000, 10000, 10000, 5000, 0, '', '', '', '1;0,0,0,0,0,0,0,0,0,0,0', '0,0,0,0,0,0,0,0,0,0', '78583a', '95d9d6', 1552510236, '{}', '5.1,6.1,7.1,8.1,35.1,36.1,37.1,26.1,27.1,28.1,29.1,30.1,31.1,32.1,33.1,34.1,38.1,39.1,40.1,41.1,72.1,73.1,74.1,75.1,76.1,77.1,78.1,79.1,80.1,81.1,82.1,83.1,84.1,85.1,86.1,87.1,88.1,89.1,90.1,91.1,92.1,234.1,235.1,236.1,237.1,238.1,93.1', '9.1,10.1,11.1,12.1,42.1,43.1,44.1,45.1,46.1,47.1,48.1,49.1,50.1,51.1,52.1,53.1,54.1,55.1,56.1,57.1,58.1,59.1,60.1,61.1,62.1,63.1,64.1,65.1,66.1,67.1,68.1,69.1,231.1,232.1,233.1', '1.1,2.1,3.1,4.1,13.1,14.1,15.1,16.1,17.1,18.1,19.1,20.1,21.1,22.1,23.1,24.1,25.1,94.1,95.1,96.1', '', '256.5,257.5,258.5,259.5,260.5,261.5,262.5,263.5,264.5,265.5,266.5,267.5,268.5,269.5,270.5,271.5,272.5,273.5,274.5,275.5,276.5,277.5,278.5,279.5,280.5,281.5,282.5,283.5,284.5,285.5,286.5', '213.1,214.1,215.1,216.1,217.1', '324.1,325.1,326.1,327.1,328.1', '', 0, 100, 0, 100, '', 25876519, '', '', 0, 0, '', 0, 0, 0, '', '', '0,0,0,0', '0,0,0,0', '2256:5;2379:5;2252:5;2349:5;23:10', '', 0, 1552591161, '', 0, 0, 0, '', '', '', 0, 0, '2,8,0,0,0,189,133,0,0', 0, 'FR', '0#0#0#0#0#0', '', '', '', '24:0', 0, 'xx', '0.jpg', 1, '', '0', '0', '0', '', '0', 1, 'qsdq@qsdqs.com', '5,3,6,1', 4, '', 0, 0, 'Little Mouse', 245, 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
