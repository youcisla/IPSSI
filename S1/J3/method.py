class Person:
    def __init__(self, name, age):
        """Initialise un objet Person avec un nom et un âge."""
        self.name = name
        self.age = age
 
    def __str__(self):
        """Retourne une représentation lisible de l'objet."""
        return f"{self.name}, {self.age} ans"
 
    def __repr__(self):
        """Retourne une représentation détaillée de l'objet pour le debugging."""
        return f"Person(name='{self.name}', age={self.age})"
 
    def __eq__(self, other):
        """Vérifie si deux objets Person ont le même nom et le même âge."""
        if isinstance(other, Person):
            return self.name == other.name and self.age == other.age
        return False
 
    def __add__(self, other):
        """Additionne l'âge de deux personnes et crée une nouvelle personne."""
        if isinstance(other, Person):
            new_name = f"{self.name} & {other.name}"
            new_age = self.age + other.age
            return Person(new_name, new_age)
        raise TypeError("L'addition n'est possible qu'entre deux objets Person")
 
    def __len__(self):
        """Retourne la longueur du nom."""
        return len(self.name)


class Livre:
    def __init__(self, auteur, annee, titre, disponible=True):
        self.auteur = auteur
        self.annee = annee
        self.titre = titre
        self.disponible = disponible

    def __str__(self):
        # Présente l'oeuvre avec l'année et le titre du livre
        return f"{self.annee} - {self.titre}"

    def emprunter(self):
        # Fonction pour emprunter le livre
        if self.disponible:
            self.disponible = False
            return f"Le livre '{self.titre}' a été emprunté."
        else:
            print("Ce n'est pas possible.")

    def rendre(self):
        # Fonction pour rendre le livre
        if not self.disponible:
            self.disponible = True
            return f"Le livre '{self.titre}' a été rendu."
        else:
            print("Le livre est déjà disponible.")


class Bibliotheque:
    def __init__(self, nom, categorie):
        self.nom = nom
        self.categorie = categorie
        self.livres = []
    
    def ajouter_livre(self, livre):
        self.livres.append(livre)
    
    def afficher_livres(self):
        if self.livres:
            return "\n".join(str(livre) for livre in self.livres)
        return "Aucun livre dans la bibliotheque."
    
    def __str__(self):
        return f"Bibliotheque {self.nom} [{self.categorie}]"


class Roman(Livre):
    def __init__(self, auteur, annee, titre, genre, disponible=True):
        super().__init__(auteur, annee, titre, disponible)
        self.genre = genre

    def __str__(self):
        base = super().__str__()
        return f"{base} - Genre: {self.genre}"


class Manuel_scolaire(Livre):
    def __init__(self, auteur, annee, titre, niveau, disponible=True):
        super().__init__(auteur, annee, titre, disponible)
        self.niveau = niveau

    def afficher_niveau(self):
        return f"Manuel destiné au niveau scolaire: {self.niveau}"

    def __str__(self):
        base = super().__str__()
        return f"{base} - Niveau scolaire: {self.niveau}"


if __name__ == "__main__":
    # Tester la classe Person
    a = Person("Alice", 30)
    b = Person("Bob", 25)
    print(a)             # Affichage lisible
    print(repr(a))       # Affichage détaillé
    print(a == b)        # False
    c = Person("Alice", 30)
    print(a == c)        # True
    couple = a + b
    print(couple)        # Alice & Bob, 55 ans
    print(len(a))        # Longueur du nom "Alice"

    # Créer quelques objets Livre
    livre1 = Livre("Victor Hugo", 1862, "Les Misérables", True)
    livre2 = Livre("Jules Verne", 1870, "Vingt mille lieues sous les mers", False)
    
    # Démonstration des méthodes emprunter et rendre
    print(livre1.emprunter())  # Devrait emprunter le livre
    print(livre1.emprunter())  # Devrait afficher message d'erreur ("Ce n'est pas possible.")
    print(livre1.rendre())      # Devrait rendre le livre
    print(livre1.rendre())      # Devrait afficher message d'erreur ("Le livre est déjà disponible.")
    
    # Créer une bibliotheque et ajouter quelques livres dont des Romans et Manuels scolaires
    bibliotheque = Bibliotheque("2B", "Action")
    bibliotheque.ajouter_livre(livre1)
    bibliotheque.ajouter_livre(livre2)

    roman1 = Roman("George Orwell", 1949, "1984", "Dystopie", True)
    manuel1 = Manuel_scolaire("Ed. Hachette", 2021, "Mathématiques Niveau 3", "Troisième")
    bibliotheque.ajouter_livre(roman1)
    bibliotheque.ajouter_livre(manuel1)
    
    # Afficher la bibliotheque et ses livres
    print(bibliotheque)
    print("Livres dans la bibliotheque :")
    print(bibliotheque.afficher_livres())
    
    # Affichage du niveau d'un manuel scolaire
    print(manuel1.afficher_niveau())