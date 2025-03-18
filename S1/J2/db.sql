-- Create the database 'db' if it doesn't already exist.
CREATE DATABASE IF NOT EXISTS db;

-- Switch to the 'db' database.
USE db;

-- Create table 'clients' with columns id, nom, email, and date_inscription.
CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Auto-incrementing primary key.
    nom VARCHAR(50) NOT NULL,             -- Client's name (required).
    email VARCHAR(100),                   -- Client's email address.
    date_inscription DATE                 -- Date of inscription.
);

-- Create table 'users' with columns id, nom, prenom, age, and profession.
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Auto-incrementing primary key.
    nom VARCHAR(50) NOT NULL,            -- User's last name (required).
    prenom VARCHAR(50),                  -- User's first name.
    age INT,                            -- User's age.
    profession VARCHAR(100)              -- User's profession.
);

-- Insert sample records into the 'users' table.
INSERT INTO users (nom, prenom, age, profession) VALUES ('Doe', 'John', 25, 'Développeur');
INSERT INTO users (nom, prenom, age, profession) VALUES ('Doe', 'Jane', 30, 'Designer');
INSERT INTO users (nom, prenom, age, profession) VALUES ('Doe', 'Alice', 18, 'Chef de projet');
INSERT INTO users (nom, prenom, age, profession) VALUES ('Doe', 'Nabile', 18, 'Technicien de surface');
INSERT INTO users (nom, prenom, age, profession) VALUES ('Doe', 'Maroua', 18, 'Chef de cuisine');

-- Select and display all 'nom' values from the 'users' table.
SELECT nom FROM users;

-- Select and display 'nom' from users who are 18 years old.
SELECT nom FROM users WHERE age = 18;

-- Select and display 'nom' values ordered by age in ascending order.
SELECT nom FROM users ORDER BY age ASC;

-- Select and display the first two 'nom' values ordered by age in ascending order.
SELECT nom FROM users ORDER BY age ASC LIMIT 2;

-- Select and display 'nom' from users aged 18, ordered alphabetically (ascending).
SELECT nom FROM users WHERE age = 18 ORDER BY nom ASC;

-- Select and display 'nom' from users aged 18, ordered alphabetically (descending).
SELECT nom FROM users WHERE age = 18 ORDER BY nom DESC;

-- Update the last name 'Doe' to 'NotDoe' for all records in the 'users' table.
UPDATE users SET nom = 'NotDoe' WHERE nom = 'Doe';

-- Delete records in the 'users' table where the last name is 'NotDoe'.
DELETE FROM users WHERE nom = 'NotDoe';