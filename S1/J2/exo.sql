-- Run in terminal : mysql -u root -p
SHOW DATABASES;
CREATE DATABASE IF NOT EXISTS MaPremiereBDD;
USE MaPremiereBDD;
CREATE TABLE IF NOT EXISTS Utilisateurs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(50) NOT NULL,
  prenom VARCHAR(50) NOT NULL,
  age INT
);
DESCRIBE Utilisateurs;
SHOW COLUMNS FROM Utilisateurs;
INSERT INTO Utilisateurs (nom, prenom, age) VALUES
('Dupont', 'Marie', 25),
('Bernard', 'Jean', 42),
('Martin', 'Sophie', 22),
('Legrand', 'Alice', 30),
('Moreau', 'Paul', 30);
SELECT * FROM Utilisateurs;my
SELECT * FROM Utilisateurs WHERE age = 30;
SELECT * FROM Utilisateurs ORDER BY nom ASC;
SELECT * FROM Utilisateurs ORDER BY nom ASC LIMIT 2;
UPDATE Utilisateurs SET age = 26 WHERE nom = 'Dupont' AND prenom = 'Marie';
SELECT * FROM Utilisateurs WHERE nom = 'Dupont' AND prenom = 'Marie';
DELETE FROM Utilisateurs WHERE id = 5;
SELECT * FROM Utilisateurs;

-- Output:
-- Enter password: ****
-- Welcome to the MySQL monitor.  Commands end with ; or \g.
-- Your MySQL connection id is 27
-- Server version: 8.0.41 MySQL Community Server - GPL

-- Copyright (c) 2000, 2025, Oracle and/or its affiliates.

-- Oracle is a registered trademark of Oracle Corporation and/or its
-- affiliates. Other names may be trademarks of their respective
-- owners.

-- Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

-- mysql> SHOW DATABASES;
-- +--------------------+
-- | Database           |
-- +--------------------+
-- | db                 |
-- | information_schema |
-- | mysql              |
-- | performance_schema |
-- | sakila             |
-- | sys                |
-- | world              |
-- +--------------------+
-- 7 rows in set (0.02 sec)

-- mysql> CREATE DATABASE IF NOT EXISTS MaPremiereBDD;
-- Query OK, 1 row affected (0.02 sec)

-- mysql> USE MaPremiereBDD;
-- Database changed
-- mysql> CREATE TABLE IF NOT EXISTS Utilisateurs (
--     ->   id INT AUTO_INCREMENT PRIMARY KEY,
--     ->   nom VARCHAR(50) NOT NULL,
--     ->   prenom VARCHAR(50) NOT NULL,
--     ->   age INT
--     -> );
-- Query OK, 0 rows affected (0.10 sec)

-- mysql> DESCRIBE Utilisateurs;
-- +--------+-------------+------+-----+---------+----------------+
-- | Field  | Type        | Null | Key | Default | Extra          |
-- +--------+-------------+------+-----+---------+----------------+
-- | id     | int         | NO   | PRI | NULL    | auto_increment |
-- | nom    | varchar(50) | NO   |     | NULL    |                |
-- | prenom | varchar(50) | NO   |     | NULL    |                |
-- | age    | int         | YES  |     | NULL    |                |
-- +--------+-------------+------+-----+---------+----------------+
-- 4 rows in set (0.00 sec)

-- mysql> SHOW COLUMNS FROM Utilisateurs;
-- +--------+-------------+------+-----+---------+----------------+
-- | Field  | Type        | Null | Key | Default | Extra          |
-- +--------+-------------+------+-----+---------+----------------+
-- | id     | int         | NO   | PRI | NULL    | auto_increment |
-- | nom    | varchar(50) | NO   |     | NULL    |                |
-- | prenom | varchar(50) | NO   |     | NULL    |                |
-- | age    | int         | YES  |     | NULL    |                |
-- +--------+-------------+------+-----+---------+----------------+
-- 4 rows in set (0.00 sec)

-- mysql> INSERT INTO Utilisateurs (nom, prenom, age) VALUES
--     -> ('Dupont', 'Marie', 25),
--     -> ('Bernard', 'Jean', 42),
--     -> ('Martin', 'Sophie', 22),
--     -> ('Legrand', 'Alice', 30),
--     -> ('Moreau', 'Paul', 30);
-- Query OK, 5 rows affected (0.01 sec)
-- Records: 5  Duplicates: 0  Warnings: 0

-- mysql> SELECT * FROM Utilisateurs;
-- +----+---------+--------+------+
-- | id | nom     | prenom | age  |
-- +----+---------+--------+------+
-- |  1 | Dupont  | Marie  |   25 |
-- |  2 | Bernard | Jean   |   42 |
-- |  3 | Martin  | Sophie |   22 |
-- |  4 | Legrand | Alice  |   30 |
-- |  5 | Moreau  | Paul   |   30 |
-- +----+---------+--------+------+
-- 5 rows in set (0.00 sec)

-- mysql> SELECT * FROM Utilisateurs WHERE age = 30;
-- +----+---------+--------+------+
-- | id | nom     | prenom | age  |
-- +----+---------+--------+------+
-- |  4 | Legrand | Alice  |   30 |
-- |  5 | Moreau  | Paul   |   30 |
-- +----+---------+--------+------+
-- 2 rows in set (0.00 sec)

-- mysql> SELECT * FROM Utilisateurs ORDER BY nom ASC;
-- +----+---------+--------+------+
-- | id | nom     | prenom | age  |
-- +----+---------+--------+------+
-- |  2 | Bernard | Jean   |   42 |
-- |  1 | Dupont  | Marie  |   25 |
-- |  4 | Legrand | Alice  |   30 |
-- |  3 | Martin  | Sophie |   22 |
-- |  5 | Moreau  | Paul   |   30 |
-- +----+---------+--------+------+
-- 5 rows in set (0.00 sec)

-- mysql> SELECT * FROM Utilisateurs ORDER BY nom ASC LIMIT 2;
-- +----+---------+--------+------+
-- | id | nom     | prenom | age  |
-- +----+---------+--------+------+
-- |  2 | Bernard | Jean   |   42 |
-- |  1 | Dupont  | Marie  |   25 |
-- +----+---------+--------+------+
-- 2 rows in set (0.00 sec)

-- mysql> UPDATE Utilisateurs SET age = 26 WHERE nom = 'Dupont' AND prenom = 'Marie';
-- Query OK, 1 row affected (0.00 sec)
-- Rows matched: 1  Changed: 1  Warnings: 0

-- mysql> SELECT * FROM Utilisateurs WHERE nom = 'Dupont' AND prenom = 'Marie';
-- +----+--------+--------+------+
-- | id | nom    | prenom | age  |
-- +----+--------+--------+------+
-- |  1 | Dupont | Marie  |   26 |
-- +----+--------+--------+------+
-- 1 row in set (0.00 sec)

-- mysql> DELETE FROM Utilisateurs WHERE id = 5;
-- Query OK, 1 row affected (0.00 sec)

-- mysql> SELECT * FROM Utilisateurs;
-- +----+---------+--------+------+
-- | id | nom     | prenom | age  |
-- +----+---------+--------+------+
-- |  1 | Dupont  | Marie  |   26 |
-- |  2 | Bernard | Jean   |   42 |
-- |  3 | Martin  | Sophie |   22 |
-- |  4 | Legrand | Alice  |   30 |
-- +----+---------+--------+------+
-- 4 rows in set (0.00 sec)

-- mysql>