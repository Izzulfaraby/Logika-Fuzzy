-- ==========================================================
-- Praktikum 3 - database fuzzy_modul1
-- Variabel usia: Anak, Remaja, Dewasa  (semesta 0 <= usia <= 150)
-- Database hanya menyimpan interval dan NAMA fungsi, bukan nilai mu(x).
-- ==========================================================
CREATE DATABASE IF NOT EXISTS fuzzy_modul1;
USE fuzzy_modul1;

DROP TABLE IF EXISTS usia_anak;
DROP TABLE IF EXISTS usia_remaja;
DROP TABLE IF EXISTS usia_dewasa;

-- ---------------- ANAK (bahu kiri) ----------------
-- 0..6 -> 1 ; 6..12 -> turun (12-x)/6 ; 12..150 -> 0
CREATE TABLE usia_anak (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usia_min INT NOT NULL,
    usia_max INT NOT NULL,
    nilai_fuzzy VARCHAR(50) NOT NULL
);
INSERT INTO usia_anak (usia_min, usia_max, nilai_fuzzy) VALUES
(0, 6, '1'),
(6, 12, 'fungsi_anak_turun'),
(12, 150, '0');

-- ---------------- REMAJA (segitiga 10-15-20, sesuai contoh modul) ----------------
CREATE TABLE usia_remaja (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usia_min INT NOT NULL,
    usia_max INT NOT NULL,
    nilai_fuzzy VARCHAR(50) NOT NULL
);
INSERT INTO usia_remaja (usia_min, usia_max, nilai_fuzzy) VALUES
(0, 10, '0'),
(10, 15, 'fungsi_remaja_naik'),
(15, 20, 'fungsi_remaja_turun'),
(20, 150, '0');

-- ---------------- DEWASA (bahu kanan) ----------------
-- 0..18 -> 0 ; 18..25 -> naik (x-18)/7 ; 25..150 -> 1
CREATE TABLE usia_dewasa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usia_min INT NOT NULL,
    usia_max INT NOT NULL,
    nilai_fuzzy VARCHAR(50) NOT NULL
);
INSERT INTO usia_dewasa (usia_min, usia_max, nilai_fuzzy) VALUES
(0, 18, '0'),
(18, 25, 'fungsi_dewasa_naik'),
(25, 150, '1');

SELECT * FROM usia_anak;
SELECT * FROM usia_remaja;
SELECT * FROM usia_dewasa;
