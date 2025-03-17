# Variables et Types
def exercice_01():
    prenom = "Youcef"
    age = 24
    taille = 1.73
    print(f"Je m'appelle {prenom}, j'ai {age} ans et je mesure {taille}m.")

# Conditions
def exercice_02():
    nombre = int(input("Veuillez saisir un nombre entier: "))
    if (nombre > 0):
        print("Le nombre est positif.")
    elif (nombre < 0):
        print("Le nombre est négatif.")
    else:
        print("Le nombre est nul.")

# Boucles
def exercice_03():
    print("nombres pairs de 1 à 20 :")
    for i in range(2, 21, 2):
        print(i, end=" ")
    print()

    nombre = int(input("\nVeuillez saisir un nombre entier pour le compte à rebours: "))
    print("compte à rebours :")
    while nombre > 0:
        print(nombre)
        nombre -= 1
    print(nombre)

# Listes et Dictionnaires
def exercice_04():
    fruits = ["pomme", "banane", "orange", "kiwi", "raisin"]
    fruits.append("mangue")
    fruits.remove("orange")
    print(fruits)

    personne = {
        "nom": "Lucas",
        "âge": 30,
        "ville": "Paris"
    }
    personne["profession"] = "Développeur"
    personne["âge"] = 31
    del personne["ville"]
    print(personne)

# Fonctions
def exercice_05():
    def carre(n):
        return n ** 2

    def somme_liste(liste):
        return sum(liste)

    def est_pair(n):
        return n % 2 == 0

    print(carre(4))
    print(somme_liste([1, 2, 3, 4, 5]))
    print(est_pair(4))
    print(est_pair(7))

# Fonction avec Paramètres Optionnels
def salutation(nom, message="Bonjour"):
    print(f"{message}, {nom}")

# Détection de Sous-Suites Strictement Croissantes
def exercice_bonus_01_version_1():
    def sous_suites_croissantes(liste):
        if len(liste) < 2:
            return
        else:
            debut = liste[0]
            reste = liste[1:]
            fin = liste[-1]
            reste2 = liste[1:-1]
            if reste and reste2 and debut < reste[0] and fin > reste2[-1]:
                print(reste)
                print(liste[:-1])
                sous_suites_croissantes(reste)
                sous_suites_croissantes(liste[:-1])
            else:
                sous_suites_croissantes(reste)
                sous_suites_croissantes(liste[:-1])
    sous_suites_croissantes([1, 2, 3, 4, 5, 6])

# Détection de Sous-Suites Strictement Croissantes
def exercice_bonus_01_version_2():
    L = [1, 2, 3, 4, 5, 6]
    result = []
    def sous_suites_croissantes(liste):
        if len(liste) < 2:
            return
        debut = liste[0]
        reste = liste[1:]
        fin = liste[-1]
        reste2 = liste[1:-1]
        if reste and reste2 and debut < reste[0] and fin > reste2[-1]:
            result.append(reste)
            result.append(liste[:-1])
            sous_suites_croissantes(reste)
            sous_suites_croissantes(liste[:-1])
        else:
            sous_suites_croissantes(reste)
            sous_suites_croissantes(liste[:-1])
    sous_suites_croissantes(L)
    unique = []
    for r in result:
        if r not in unique:
            unique.append(r)
    tails, others = [], []
    for s in unique:
        idx = L.index(s[0])
        if s == L[idx:]:
            tails.append((idx, s))
        else:
            others.append((idx, len(s), s))
    tails.sort(key=lambda x: x[0])
    others.sort(key=lambda x: (x[1], -x[0]))
    final = [s for _, s in tails] + [s for _, _, s in others]
    for s in final:
        print(s)

# Compression de Chaine (Run-Length Encoding)
def run_length_encoding(chaine):
    if not chaine:
        return ""
    resultat = []
    compteur = 1
    for i in range(len(chaine) - 1):
        if chaine[i] == chaine[i + 1]:
            compteur += 1
        else:
            resultat.append(chaine[i] + str(compteur))
            compteur = 1
    resultat.append(chaine[-1] + str(compteur))
    return "".join(resultat)

def run_length_decoding(chaine):
    resultat = []
    i = 0
    while i < len(chaine):
        caractere = chaine[i]
        i += 1
        nombre = ""
        while i < len(chaine) and chaine[i].isdigit():
            nombre += chaine[i]
            i += 1
        resultat.append(caractere * int(nombre))
    return "".join(resultat)

# Tests
if __name__ == "__main__":
    separator = "\n" + "="*30 + "\n"

    print(separator + "Test: Exercice 01" + separator)
    exercice_01()
    
    print(separator + "Test: Exercice 02 (input required)" + separator)
    exercice_02()
    
    print(separator + "Test: Exercice 03 (input required)" + separator)
    exercice_03()
    
    print(separator + "Test: Exercice 04" + separator)
    exercice_04()
    
    print(separator + "Test: Exercice 05" + separator)
    exercice_05()
    
    print(separator + "Test: Salutation" + separator)
    salutation("Youcef")
    salutation("Youcef", message="Salut")
    
    print(separator + "Test: Exercice Bonus 01 Version 1" + separator)
    exercice_bonus_01_version_1()
    
    print(separator + "Test: Exercice Bonus 01 Version 2" + separator)
    exercice_bonus_01_version_2()
    
    print(separator + "Test: Run-Length Encoding & Decoding" + separator)
    test_str = "aaabbcddd"
    encoded = run_length_encoding(test_str)
    print("Encoded:", encoded)
    decoded = run_length_decoding(encoded)
    print("Decoded:", decoded)
