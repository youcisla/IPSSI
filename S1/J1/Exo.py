import math

def toFahrenheit():
    user_input = input("Entrez la température en Celsius : ")
    celsius = float(user_input)
    fahrenheit = (celsius * 9/5) + 32
    print(f"La température en Fahrenheit est de : {fahrenheit}")

def circonference():
    user_input = input("Entrez le rayon du cercle : ")
    rayon = float(user_input)
    circonference = rayon * 2 * math.pi
    print(f"la circonférence du cercle est de : {circonference}")

def salaire():
    heures = input("Entrez le nombre d'heures : ")
    taux = input("Entrez le taux horaire : ")
    salaire = int(taux) * int(heures)
    print(f"Votre gain hebdomadaire est de : {salaire}")

def IMC():
    poids = input("Entrez votre poids en kg : ")
    taille = input("Entrez votre taille en mètres : ")
    IMC = float(poids) / (float(taille) ** 2)
    print(f"Votre gain hebdomadaire est de : {IMC}")