"""Ce script permet de définir les fonctions qui vont vérifier la validité des données entrées par l'utilisateur"""
from gestion_BDD_fluides import *
import numpy as np

# Définition de la procédure nettoyer_écran
def nettoyer_ecran():
    """Cette procédure permet de nettoyer la console, afin que rien n'y soit plus affiché"""
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


# Définition de la fonction qui vérifie que l'entrée est une section valable
def get_element_liste_input(liste):
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


def get_choix_mode():
    print("Que voulez-vous faire dans ce programme ?")
    print("1 - Étudier un problème de canalisation")
    print("2 - Ajouter/supprimer un matériau à la base de données")
    print("3 - Ajouter/supprimer un fluide à la base de données")
    print("Entrez 1, 2 ou 3.")
    value = input("--> ")
    liste = ['1', '2', '3']
    while value not in liste:
        print("Entrée invalide, vous devez entrer 1, 2 ou 3.")
        value = input("--> ")
    return int(value)


def get_init_cond_input(fluide, diametre):
    liste_temperature = recuperer_liste_temperature(fluide)
    print("Voulez-vous entrez la vitesse (m/s) ou le débit (m3/s) à l'entrée de la canalisation ?")
    choix = get_element_liste_input(['vitesse','débit'])
    if choix == 'débit':
        print("Veuillez entrer le débit en m3/s")
        debit = get_float_input('+')
        vitesse = debit/(np.pi*(diametre/2)**2)
    else:
        print("Quelle est la vitesse initiale, en m/s ?")
        vitesse = get_float_input('+')

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
        densite = 0
        viscosite_cine = 0

    return vitesse, temperature, pression, densite, viscosite_cine

def get_float_between_input(a,b):
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