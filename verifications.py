"""Ce script permet de définir les fonctions qui vont vérifier la validité des données entrées par l'utilisateur"""
from gestion_BDD_fluides import *
import numpy as np

# Définition de la procédure nettoyer_écran
def nettoyer_ecran():
    """
    Cette procédure permet de nettoyer la console

    Args :
        Aucun

    Returns :
        Aucun
    """
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")


# Définition de la fonction qui vérifie que l'entrée est bien un flottant
# La fonction est inspirée de celle définie dans le module 09 - Introduction à la POO
def get_float_input(signe='all'):
    """
    Cette fonction permet de récupérer un flottant, qu'a entré l'utilisateur

    Args :
        signe (str) : '+' pour des flottants supérieurs ou égaux à 0, '-' sinon

    Returns :
        float : Le flottant entré par l'utilisateur
    """
    while True:
        # On vérifie constamment l'entrée
        try:
            # On demande à l'utilisateur d'entrer la valeur
            entree = input("--> ")
            # On essaie de le convertir en flottant, si ca ne marche pas, on va dans "except"
            value = float(entree)
            if (value >= 0 and signe == '+') or (value <= 0 and signe == '-') or signe == 'all':
                break
            else:
                print("\n Entrée invalide, le signe du nombre entré n'est pas correct. Essayez à nouveau.")
        except ValueError:
            # Si l'entrée n'est pas un flottant, on obtient ValueError
            print("\n Entrée invalide, elle doit être un décimal. Essayez à nouveau.")
    return value


# Définition de la fonction qui vérifie que l'entrée est bien un entier
# Fonction inspirée de la fonction vérifiant les flottants
def get_int_input(signe='all'):
    """
    Cette fonction permet de récupérer un entier, qu'a entré l'utilisateur

    Args :
        signe (str) : '+' pour des flottants supérieurs ou égaux à 0, '-' sinon

    Returns :
        int : L'entier entré par l'utilisateur
    """
    while True:
        # On vérifie constamment l'entrée
        try:
            # On demande à l'utilisateur d'entrer la valeur
            entree = input("--> ")
            # On essaie de le convertir en entier, si ca ne marche pas, on va dans "except"
            value = int(entree)
            if (value >= 0 and signe == '+') or (value < 0 and signe == '-') or signe == 'all':
                break
            else:
                print("\n Entrée invalide, le signe du nombre entré n'est pas correct. Essayez à nouveau.")
        except ValueError:
            # Si l'entrée n'est pas un entier, on obtient ValueError
            print(" \nEntrée invalide, elle doit être un entier. Essayez à nouveau.")
    return value


def get_element_liste_input(liste):
    """
    Cette fonction permet de récupérer un élément d'une liste, entré par l'utilisateur

    Args :
        liste (list) : La liste des choix donnés à l'utilisateur

    Returns :
        str : Le choix de l'utilisateur
    """
    mots_chaine = liste[0]
    for i in liste[1:]:
        mots_chaine += ', '
        mots_chaine += (i)
    print(f"Veuillez choisir parmi : ")
    print(mots_chaine)
    value = input("--> ")
    while value not in liste:
        print("Entrée invalide, vous devez sélectionner un élément de la liste :")
        print(mots_chaine)
        value = input("--> ")
    return value


def get_init_cond_input(fluide, diametre):
    """
    Cette fonction permet de récupérer les conditions initiales, entrées par l'utilisateur

    Args :
        fluide (str) : Le nom du fluide
        diametre (float) : Le diamètre de la canalisation

    Returns :
        float : La vitesse initiale du fluide, en m/s
        float : La température initiale du fluide, en °C
        float : La pression initiale du fluide, en Pa
        float : La densité du fluide, en kg/m883
        float : La viscosité cinématique du fluide, en m**2/s
        float : Le débit du fluide, en m**3/s
    """

    liste_temperature = recuperer_liste_temperature(fluide)
    print("Voulez-vous entrez la vitesse (m/s) ou le débit (m3/s) à l'entrée de la canalisation ?")
    choix = get_element_liste_input(['vitesse','débit'])
    if choix == 'débit':
        print("Veuillez entrer le débit en m3/s")
        debit = get_float_input('+')
        vitesse = debit / (np.pi * (diametre/2)**2)
    else:
        print("Quelle est la vitesse initiale, en m/s ?")
        vitesse = get_float_input('+')
        debit = vitesse * np.pi * (diametre/2)**2

    print("Quelle est la température initiale, en °C ?")
    temperature = get_float_input()
    while temperature < min(liste_temperature) or temperature > max(liste_temperature):
        print(f"La température initiale doit être comprise entre {min(liste_temperature)} °C et {max(liste_temperature)} °C ")
        print(f"La température initiale actuelle vaut {temperature} °C, veuillez la modifier.")
        temperature = get_float_input('+')

    print("Le programme s'appuie sur une base de donnée pour effectuer ses calculs.")
    print("Vous pouvez en faire abstraction et utiliser vos propres données.")
    print("Connaissez-vous les paramètre de votre fluide : densité, viscosité cinématique, pression ?")
    choix_donnees = get_element_liste_input(['oui','non'])
    if choix_donnees == 'oui':
        print("Que vaut la pression initiale, en bar ?")
        pression = get_float_input('+')*10**5
        print("Que vaut la densité initiale, en kg/m3 ?")
        densite = get_float_input('+')
        print("Que vaut la viscosité cinématique initiale, en m2/s ?")
        viscosite_cine = get_float_input('+')
    else:
        print("La pression initiale est fixée à "
              "la pression atmosphérique : 1,013 en bar.")
        pression = 1.013*10**5
        densite = recuperer_valeur_fluide(fluide, temperature, 'Masse volumique')
        viscosite_cine = recuperer_valeur_fluide(fluide, temperature, 'Viscosité cinématique')

    return vitesse, temperature, pression, densite, viscosite_cine, debit


def get_float_between_input(a,b):
    """
    Cette fonction permet de récupérer un flottant dans un intervalle, entrées par l'utilisateur

    Args :
        a (float) : Le plus petit nombre de l'intervalle
        b (float) : Le plus grand nombre de l'intervalle

    Returns :
        float : Le nombre entré par l'utilisateur, dans l'intervalle
    """
    while b < a:
        print(f"{b} est plus petit que {a}, veuillez entrez à nouveau les bornes")
        print("a = ")
        a = get_float_input()
        print("b = ")
        b = get_float_input()
    nbre = get_float_input()
    while nbre > b or nbre < a:
        print("Le chiffre entré n'est pas dans l'intervalle, veuillez le saisir à nouveau.")
        nbre = get_float_input()
    return nbre


def get_int_between_input(a,b):
    """
    Cette fonction permet de récupérer un entier dans un intervalle, entrées par l'utilisateur

    Args :
        a (float) : Le plus petit nombre de l'intervalle
        b (float) : Le plus grand nombre de l'intervalle

    Returns :
        int : Le nombre entré par l'utilisateur, dans l'intervalle
    """
    while b < a:
        print(f"{b} est plus petit que {a}, veuillez entrez à nouveau les bornes")
        print("a = ")
        a = get_int_input()
        print("b = ")
        b = get_float_input()
    nbre = get_int_input()
    while nbre > b or nbre < a:
        print(f"Le chiffre entré n'est pas dans l'intervalle [{a};{b}], veuillez le saisir à nouveau.")
        nbre = get_int_input()
    return nbre