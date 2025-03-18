-- 1. Création de la Base de Données et des Tables
-- Création de la base de données
CREATE DATABASE Gestion_Tickets_IT;

USE Gestion_Tickets_IT;

-- Table Employes
CREATE TABLE Employes (
    id INT AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

-- Table Techniciens
CREATE TABLE Techniciens (
    id INT AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    specialite VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

-- Table Statuts
CREATE TABLE Statuts (
    id INT AUTO_INCREMENT,
    libelle VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

-- Table Priorites
CREATE TABLE Priorites (
    id INT AUTO_INCREMENT,
    niveau VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

-- Table Tickets
CREATE TABLE Tickets (
    id INT AUTO_INCREMENT,
    titre VARCHAR(255) NOT NULL,
    description TEXT,
    date_ouverture DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_fermeture DATETIME DEFAULT NULL,
    temps_resolution TIME DEFAULT NULL,
    id_statut INT NOT NULL,
    id_priorite INT NOT NULL,
    id_employe INT NOT NULL,
    id_technicien INT DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_statut) REFERENCES Statuts (id),
    FOREIGN KEY (id_priorite) REFERENCES Priorites (id),
    FOREIGN KEY (id_employe) REFERENCES Employes (id),
    FOREIGN KEY (id_technicien) REFERENCES Techniciens (id)
);

-- 2. Insertion de Données
-- Insertion dans Employes (au moins 5)
INSERT INTO Employes (nom, email) VALUES 
('Alice Dupont', 'alice.dupont@example.com'),
('Bob Martin', 'bob.martin@example.com'),
('Claire Bernard', 'claire.bernard@example.com'),
('David Lefevre', 'david.lefevre@example.com'),
('Emma Moreau', 'emma.moreau@example.com');

-- Insertion dans Techniciens (3 techniciens aux spécialités différentes)
INSERT INTO Techniciens (nom, specialite) VALUES 
('Tech One', 'Réseau'),
('Tech Two', 'Hardware'),
('Tech Three', 'Software');

-- Insertion dans Statuts
INSERT INTO Statuts (libelle) VALUES 
('Ouvert'),
('En cours'),
('Résolu'),
('Fermé');

-- Insertion dans Priorites
INSERT INTO Priorites (niveau) VALUES 
('Faible'),
('Moyenne'),
('Haute'),
('Critique');

-- Insertion dans Tickets (10 tickets avec des combinaisons variées)
INSERT INTO Tickets (titre, description, id_statut, id_priorite, id_employe, id_technicien) VALUES 
('Ticket 1', 'Problème de connexion internet', 1, 3, 1, 1),
('Ticket 2', 'Ordinateur ne démarre pas', 2, 4, 2, 2),
('Ticket 3', 'Erreur logiciel', 1, 2, 3, 3),
('Ticket 4', 'Imprimante en panne', 1, 1, 4, 1),
('Ticket 5', 'Accès refusé', 2, 3, 5, 2),
('Ticket 6', 'Problème de mise à jour', 1, 2, 1, 3),
('Ticket 7', 'Virus détecté', 3, 4, 2, 1),
('Ticket 8', 'Problème de réseau', 1, 3, 3, 2),
('Ticket 9', 'Logiciel obsolète', 2, 1, 4, 3),
('Ticket 10', 'Chute de connexion', 1, 2, 5, 1);

-- 3. Requêtes SQL
-- 3.1 Requêtes avec jointures
-- Afficher tous les tickets avec le nom de l’employé, le statut et la priorité associée :
SELECT t.id, t.titre, t.description, t.date_ouverture, t.date_fermeture, e.nom AS employe, s.libelle AS statut, p.niveau AS priorite
FROM Tickets t
JOIN Employes e ON t.id_employe = e.id
JOIN Statuts s ON t.id_statut = s.id
JOIN Priorites p ON t.id_priorite = p.id;

-- Liste des techniciens avec le nombre de tickets qu’ils gèrent :
SELECT tech.id, tech.nom, COUNT(t.id) AS nb_tickets
FROM Techniciens tech
LEFT JOIN Tickets t ON tech.id = t.id_technicien
GROUP BY tech.id, tech.nom;

-- Afficher les tickets en cours avec le nom du technicien et de l’employé associé :
SELECT t.id, t.titre, e.nom AS employe, tech.nom AS technicien
FROM Tickets t
JOIN Employes e ON t.id_employe = e.id
JOIN Techniciens tech ON t.id_technicien = tech.id
JOIN Statuts s ON t.id_statut = s.id
WHERE s.libelle = 'En cours';

-- 3.2 Requêtes avec sous-requêtes
-- Afficher les tickets ayant la priorité la plus élevée :
SELECT *
FROM Tickets
WHERE id_priorite = (SELECT id FROM Priorites WHERE niveau = 'Critique');

-- Trouver les techniciens qui ont au moins un ticket ouvert :
SELECT *
FROM Techniciens
WHERE id IN (
    SELECT id_technicien FROM Tickets
    WHERE id_statut = (SELECT id FROM Statuts WHERE libelle = 'Ouvert')
);

-- Lister les employés qui ont ouvert plus de 2 tickets :
SELECT e.id, e.nom, COUNT(t.id) AS nb_tickets
FROM Employes e
JOIN Tickets t ON e.id = t.id_employe
GROUP BY e.id, e.nom
HAVING COUNT(t.id) > 2;

-- 3.3 Requêtes avec agrégation
-- Nombre total de tickets par statut :
SELECT s.libelle AS statut, COUNT(t.id) AS nb_tickets
FROM Statuts s
LEFT JOIN Tickets t ON s.id = t.id_statut
GROUP BY s.libelle;

-- Moyenne du nombre de tickets par technicien :
SELECT AVG(nb) AS moyenne_tickets
FROM (
    SELECT COUNT(t.id) AS nb
    FROM Techniciens tech
    LEFT JOIN Tickets t ON tech.id = t.id_technicien
    GROUP BY tech.id
) AS sub;

-- Nombre de tickets créés par mois :
SELECT DATE_FORMAT(date_ouverture, '%Y-%m') AS mois, COUNT(id) AS nb_tickets
FROM Tickets
GROUP BY DATE_FORMAT(date_ouverture, '%Y-%m');

-- 4. Création d’une Vue
-- Vue vue_tickets_ouverts pour afficher uniquement les tickets non fermés :
CREATE VIEW IF NOT EXISTS vue_tickets_ouverts AS
SELECT *
FROM Tickets
WHERE id_statut <> (SELECT id FROM Statuts WHERE libelle = 'Fermé');

-- 5. Création d’une Fonction Stockée
-- Fonction nb_tickets_technicien qui retourne le nombre de tickets attribués à un technicien donné 
DELIMITER $$
CREATE FUNCTION nb_tickets_technicien(p_id_technicien INT) RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE nb INT;
    SELECT COUNT(*) INTO nb FROM Tickets WHERE id_technicien = p_id_technicien;
    RETURN nb;
END$$
DELIMITER ;

-- 6. Création d’un Trigger
-- Trigger pour mettre à jour automatiquement la date de fermeture (et le temps de résolution) lorsque le statut passe à « Fermé » 
DELIMITER $$
CREATE TRIGGER trg_ticket_ferme
AFTER UPDATE ON Tickets
FOR EACH ROW
BEGIN
    IF NEW.id_statut = (SELECT id FROM Statuts WHERE libelle = 'Fermé')
       AND OLD.id_statut <> (SELECT id FROM Statuts WHERE libelle = 'Fermé') THEN
        UPDATE Tickets
        SET date_fermeture = NOW(),
            temps_resolution = TIMEDIFF(NOW(), date_ouverture)
        WHERE id = NEW.id;
    END IF;
END$$
DELIMITER ;

-- 7. Transactions
-- Simulation d’un scénario transactionnel où un employé ouvre un ticket et un technicien est assigné 
START TRANSACTION;
    INSERT INTO Tickets (titre, description, id_statut, id_priorite, id_employe, id_technicien)
    VALUES (
        'Ticket Transaction', 
        'Problème de simulation', 
        (SELECT id FROM Statuts WHERE libelle = 'Ouvert'),
        (SELECT id FROM Priorites WHERE niveau = 'Moyenne'),
        1,
        1
    );
-- Si toutes les étapes se passent bien, on valide la transaction
COMMIT;