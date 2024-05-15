-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 15, 2024 at 07:18 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flask`
--

-- --------------------------------------------------------

--
-- Table structure for table `penjualan`
--

CREATE TABLE `penjualan` (
  `id` int(11) NOT NULL,
  `nama_barang` varchar(255) NOT NULL,
  `harga_barang` bigint(100) NOT NULL,
  `jumlah_barang` int(11) NOT NULL,
  `total_harga` bigint(100) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `penjualan`
--

INSERT INTO `penjualan` (`id`, `nama_barang`, `harga_barang`, `jumlah_barang`, `total_harga`, `created_at`, `updated_at`) VALUES
(1, 'asas', 109000, 1, 1000000, '2024-05-15 23:57:36', '2024-05-15 23:57:36'),
(2, 'aseadasd', 1231, 1, 2132123, '2024-05-16 00:02:38', '2024-05-16 00:02:38'),
(3, '1231321', 12, 21, 213232131, '2024-05-16 00:05:08', '2024-05-16 00:05:08'),
(4, 'aaaa', 1232, 2, 2222, '2024-05-16 00:09:37', '2024-05-16 00:09:37'),
(5, 'aaaa', 232, 2, 2, '2024-05-16 00:10:39', '2024-05-16 00:10:39');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `username`, `password`, `created_at`, `updated_at`) VALUES
(5, 'aa@1231', 'aaa123', '$2b$12$FPp8lWwL25kXkbnvOHn0nu/LDRBJt/yzT0LT9FVQMBCqoBOLc90y.', '2024-05-15 23:08:18', '2024-05-15 23:08:18'),
(6, 'aa@123', 'aa123', '$2b$12$97GIKUZhScPz1uRhNSqx2eZaqwT4DppZAVMmbDW0h7ZXm784rjWzK', '2024-05-15 23:12:09', '2024-05-15 23:12:09'),
(7, 'test@123', 'test123', '$2b$12$QzdlHF.47qlFbwGtP500SuAkoRjFnrMHVDtr.OwAYikpf1hfRIEvu', '2024-05-15 23:21:51', '2024-05-15 23:21:51');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `penjualan`
--
ALTER TABLE `penjualan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `penjualan`
--
ALTER TABLE `penjualan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
