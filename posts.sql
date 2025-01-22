-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 22, 2025 at 10:01 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `resourcesharing`
--

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `sno` int(11) NOT NULL,
  `resource_name` varchar(1000) NOT NULL,
  `subheading` varchar(50) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `shared_by` varchar(1000) NOT NULL,
  `date` date NOT NULL,
  `slug` varchar(50) NOT NULL,
  `img_file` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`sno`, `resource_name`, `subheading`, `description`, `shared_by`, `date`, `slug`, `img_file`) VALUES
(1, 'Straykids', 'skz', 'Stray Kids (Korean: 스트레이 키즈; RR: Seuteurei Kijeu; often abbreviated to SKZ) is a South Korean boy band formed by JYP Entertainment. The band consists of eight members: Bang Chan, Lee Know, Changbin, Hyunjin, Han, Felix, Seungmin, and I.N. For undisclosed personal reasons, Woojin left the band in October 2019. Stray Kids primarily self-produce its recordings; the main production team is named 3Racha and consists of Bang Chan, Changbin, and Han, and the other members frequently participate in songwriting.', 'felix', '2025-01-21', 'first-post', 'about-bg.jpg'),
(2, 'P1Harmony ', 'GenZ kpop culture ', 'P1Harmony is a South Korean boy band formed and managed by FNC Entertainment, consisting of Keeho, Theo, Jiung, Intak, Soul, and Jongseob. The group was introduced through the film P1H: The Beginning of a New World on August 27, 2020, and later debuted on October 28, 2020, with their first EP Disharmony: Stand Out.', 'keeho', '2025-01-21', 'second-post', 'post-bg.jpg'),
(3, 'apple', 'fruit', 'An apple is a round, edible fruit produced by an apple tree (Malus spp., among them the domestic or orchard apple; Malus domestica). Apple trees are cultivated worldwide and are the most widely grown species in the genus Malus. The tree originated in Central Asia, where its wild ancestor, Malus sieversii, is still found. Apples have been grown for thousands of years in Eurasia and were introduced to North America by European colonists. Apples have religious and mythological significance in many cultures, including Norse, Greek, and European Christian tradition.', 'felix', '2025-01-22', 'third-post', 'about-bg.jpg'),
(4, 'mango', 'fruit 2', 'A mango is an edible stone fruit produced by the tropical tree Mangifera indica. It originated from the region between northwestern Myanmar, Bangladesh, and northeastern India.[1][2] M. indica has been cultivated in South and Southeast Asia since ancient times resulting in two types of modern mango cultivars: the \"Indian type\" and the \"Southeast Asian type\".Other species in the genus Mangifera also produce edible fruits that are also called \"mangoes\", the majority of which are found in the Malesian ecoregion.[3]', 'felix', '2025-01-22', 'fourth-post', 'post-bg.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
