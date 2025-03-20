CREATE DATABASE IF NOT EXISTS tp_final;
USE tp_final;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(512) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    status ENUM('active', 'inactive') DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('open', 'closed', 'in progress', 'pending') DEFAULT 'open',
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

INSERT IGNORE INTO user (username, password_hash, role, status)
VALUES 
    ('admin', 'hashed_password_123', 'admin', 'active'),
    ('user1', 'hashed_password_234', 'user', 'active'),
    ('user2', 'hashed_password_345', 'user', 'inactive');

INSERT IGNORE INTO tickets (user_id, title, description, status)
VALUES
    (1, 'Ticket Admin 1', 'Description du ticket admin 1', 'open'),
    (1, 'Ticket Admin 2', 'Description du ticket admin 2', 'closed'),
    (2, 'Ticket User 1', 'Description du ticket user 1', 'open'),
    (2, 'Ticket User 2', 'Description du ticket user 2', 'closed');
    
INSERT IGNORE INTO tickets (user_id, title, description, status) VALUES
(1, 'Erreur de connexion au portail client', 'L''utilisateur ne parvient pas à se connecter à son espace client malgré la vérification de ses identifiants.', 'open'),
(2, 'Problème de mise à jour du logiciel', 'Lors de l''installation de la dernière mise à jour, le logiciel s''est arrêté et affiche un message d''erreur.', 'in progress'),
(3, 'Impression impossible depuis l''ordinateur', 'L''utilisateur ne peut pas imprimer depuis son poste, l''imprimante ne répond pas.', 'closed'),
(1, 'Site web inaccessible', 'Des clients signalent que le site web est très lent et parfois totalement inaccessible.', 'pending'),
(2, 'Erreur lors du paiement en ligne', 'Un client a rencontré une erreur critique lors de la validation de son paiement sur le site e-commerce.', 'open'),
(3, 'Problème de synchronisation des emails', 'Les emails ne se synchronisent plus sur l''application mobile, laissant des messages en attente.', 'in progress'),
(1, 'Bug dans l''application mobile', 'Suite à la dernière mise à jour, l''application se ferme brusquement, perturbant l''expérience utilisateur.', 'closed'),
(2, 'Défaillance du système de sauvegarde', 'Le système de sauvegarde automatique n''a pas fonctionné durant la nuit, risquant une perte de données importantes.', 'pending'),
(3, 'Problème d''impression couleur', 'L''imprimante n''imprime qu''en noir et blanc malgré la sélection de l''option couleur.', 'open'),
(1, 'Difficulté d''accès aux ressources internes', 'Certains employés ne parviennent pas à accéder aux documents partagés sur le serveur intranet.', 'in progress'),
(2, 'Message d''erreur lors du lancement du logiciel', 'Au démarrage, le logiciel de comptabilité affiche un message d''erreur systématique.', 'closed'),
(3, 'Problème de compatibilité du navigateur', 'Le site web ne s''affiche pas correctement sur certains navigateurs, notamment Internet Explorer.', 'pending'),
(1, 'Demande de réinitialisation du mot de passe', 'L''utilisateur a oublié son mot de passe et demande une procédure de réinitialisation sécurisée.', 'open'),
(2, 'Accès refusé au dossier partagé', 'Malgré des droits d''accès corrects, l''utilisateur se voit refuser l''accès au dossier partagé sur le réseau.', 'in progress'),
(3, 'Erreur de facturation', 'Une incohérence a été détectée sur le dernier relevé client, nécessitant une vérification des montants.', 'closed'),
(1, 'Incohérence dans les données du CRM', 'Les informations client ne sont pas correctement synchronisées entre le CRM et la base de données centrale.', 'pending'),
(2, 'Incident de sécurité informatique', 'Une activité suspecte a été détectée sur le réseau, indiquant une potentielle violation de la sécurité.', 'open'),
(3, 'Problème de connexion VPN', 'Plusieurs employés ne parviennent pas à se connecter au VPN, perturbant le travail à distance.', 'in progress'),
(1, 'Application de messagerie lente', 'L''application de messagerie met beaucoup de temps à envoyer et recevoir des messages, ralentissant la communication.', 'closed'),
(2, 'Dysfonctionnement du système de tickets', 'Le système de support ne crée pas de tickets pour les nouvelles demandes des utilisateurs.', 'pending'),
(3, 'Erreur lors de l''installation de l''imprimante', 'L''installation du pilote d''imprimante échoue sur plusieurs postes de travail, bloquant l''impression.', 'open'),
(1, 'Problème de mise à jour de l''OS', 'La dernière mise à jour de l''OS a entraîné des incompatibilités avec certains logiciels essentiels.', 'in progress'),
(2, 'Impossible d''envoyer des pièces jointes', 'Les emails refusent l''ajout de pièces jointes, ce qui entrave la transmission de documents.', 'closed'),
(3, 'Écran bleu sur PC', 'Un écran bleu apparaît sur l''ordinateur de l''utilisateur, nécessitant un redémarrage immédiat pour retrouver l''accès.', 'pending'),
(1, 'Problème de connectivité réseau', 'Des coupures récurrentes affectent la connexion Internet dans le bureau, perturbant le travail quotidien.', 'open'),
(2, 'Application web non responsive', 'L''application web ne s''adapte pas aux différents formats d''écran, particulièrement sur les appareils mobiles.', 'in progress'),
(3, 'Difficulté à imprimer depuis le mobile', 'La fonction d''impression via l''application mobile ne répond pas, empêchant l''impression à distance.', 'closed'),
(1, 'Bug dans le module de reporting', 'Les rapports générés contiennent des erreurs de calcul et des données incohérentes, affectant les analyses.', 'pending'),
(2, 'Problème de mise à jour de la base de données', 'La mise à jour automatique de la base de données a échoué, nécessitant une intervention manuelle.', 'open'),
(3, 'Erreur d''authentification SSO', 'Le système de Single Sign-On ne reconnaît pas les identifiants, obligeant les utilisateurs à saisir leur mot de passe.', 'in progress'),
(1, 'Demande de nouvelle fonctionnalité', 'Un utilisateur suggère l''ajout d''un filtrage avancé pour améliorer l''expérience dans l''application.', 'closed'),
(2, 'Impossibilité de sauvegarder un document', 'Les utilisateurs ne parviennent pas à enregistrer leurs documents sur le serveur de fichiers partagé.', 'pending'),
(3, 'Problème de latence lors des appels vidéo', 'Les appels vidéo via la plateforme collaborative présentent une latence excessive, perturbant les réunions.', 'open'),
(1, 'Erreur de chargement des images', 'Les images sur le site web ne se chargent pas correctement, nuisant à la navigation des utilisateurs.', 'in progress'),
(2, 'Défaillance du système de notifications', 'Les notifications en temps réel ne s''affichent pas, empêchant la réception d''alertes importantes.', 'closed'),
(3, 'Problème d''affichage des données', 'Les tableaux de bord ne se mettent pas à jour correctement après la dernière modification des données.', 'pending'),
(1, 'Erreur de synchronisation des contacts', 'Les contacts de l''application mobile ne se synchronisent pas avec le compte principal, causant des doublons.', 'open'),
(2, 'Interruption de service internet', 'Une panne générale a affecté la connexion internet dans le bureau pendant plusieurs heures.', 'in progress'),
(3, 'Incapacité à se connecter au serveur de messagerie', 'L''utilisateur ne parvient pas à établir une connexion avec le serveur de messagerie interne.', 'closed'),
(1, 'Bug dans l''outil de planification', 'L''outil de planification affiche des disponibilités erronées, créant des conflits dans l''organisation.', 'pending'),
(2, 'Problème d''intégration avec l''API', 'L''intégration avec une API tierce échoue, empêchant l''importation des données nécessaires.', 'open'),
(3, 'Erreur de configuration du routeur', 'Le routeur de l''entreprise semble mal configuré, provoquant des coupures fréquentes de connexion.', 'in progress'),
(1, 'Problème de sécurité du site web', 'Une faille de sécurité potentielle a été identifiée sur le site web, nécessitant une analyse urgente.', 'closed'),
(2, 'Demande d''assistance pour installation logiciel', 'L''utilisateur requiert une aide pour installer un nouveau logiciel sur son poste de travail.', 'pending'),
(3, 'Erreur lors de l''exportation de données', 'L''exportation des données vers Excel échoue et renvoie un message d''erreur inattendu.', 'open'),
(1, 'Problème d''accès à la base de données', 'L''utilisateur ne peut pas accéder à la base de données via le logiciel de gestion, perturbant ses opérations.', 'in progress'),
(2, 'Incident de panne électrique', 'Une panne électrique a affecté plusieurs systèmes critiques dans le bureau, nécessitant une vérification technique.', 'closed'),
(3, 'Bug dans le système de réservation', 'Le système de réservation en ligne rencontre un bug qui empêche la validation des réservations.', 'pending'),
(1, 'Problème de configuration de messagerie', 'La configuration du client de messagerie semble incorrecte, bloquant la réception des emails.', 'open'),
(2, 'Erreur de calcul dans le logiciel de facturation', 'Une erreur dans le module de facturation provoque des montants erronés sur les factures, nécessitant une correction.', 'in progress');
