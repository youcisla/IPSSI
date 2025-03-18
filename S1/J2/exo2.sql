-- Liste des 10 villes les plus peuplées en 2012
SELECT ville_nom FROM villes_france_free ORDER BY ville_population_2012 DESC LIMIT 10;

-- Liste des 50 villes ayant la plus faible superficie
SELECT ville_nom FROM villes_france_free ORDER BY ville_surface ASC LIMIT 50;

-- Récupération des départements d'outre-mer (code commence par 97)
SELECT * FROM departement WHERE departement_code LIKE '97%';

-- Affichage des 10 villes les plus peuplées en 2012 avec leur département
SELECT v.ville_nom, d.departement_nom FROM villes_france_free v JOIN departement d ON v.ville_departement = d.departement_code ORDER BY v.ville_population_2012 DESC LIMIT 10;

-- Nombre de communes par département, classé du plus grand au plus petit
SELECT d.departement_nom, d.departement_code, COUNT(v.ville_id) AS nombre_communes FROM villes_france_free v JOIN departement d ON v.ville_departement = d.departement_code GROUP BY d.departement_nom, d.departement_code ORDER BY nombre_communes DESC;

-- Liste des 10 départements ayant la plus grande superficie
SELECT departement_nom, departement_code FROM departement ORDER BY departement_surface DESC LIMIT 10;

-- Compter le nombre de villes commençant par "Saint"
SELECT COUNT(*) FROM villes_france_free WHERE ville_nom LIKE 'Saint%';

-- Villes ayant un nom partagé par plusieurs communes, classées par fréquence
SELECT ville_nom, COUNT(*) AS occurrences FROM villes_france_free GROUP BY ville_nom HAVING COUNT(*) > 1 ORDER BY occurrences DESC;

-- Liste des communes dont la superficie dépasse la moyenne
SELECT ville_nom FROM villes_france_free WHERE ville_surface > (SELECT AVG(ville_surface) FROM villes_france_free);

-- Liste des départements dont la population dépasse 2 millions d'habitants
SELECT departement_nom FROM departement WHERE departement_population > 2000000;

-- Remplacement du tiret par un espace dans les noms commençant par "SAINT-"
UPDATE villes_france_free SET ville_nom = REPLACE(ville_nom, 'SAINT-', 'SAINT ') WHERE ville_nom LIKE 'SAINT-%';