"""Ce script permet de définir les fonctions qui vont vérifier la validité des données entrées par l'utilisateur"""


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
            entree = input("-->")
            # On essaie de le convertir en flottant, si ca ne marche pas, on va dans "except"
            value = float(entree)
            if (value >= 0 and signe == '+') or (value < 0 and signe == '-') or signe == 'all':
                break
            else:
                print("\n Entrée invalide, le signe du nombre entré n'est pas correct. Essayez à nouveau.")
        except ValueError:
            # Si l'entrée n'est pas un flottant, on obtient ValueError
            print("\n Entrée invalide, elle doit être un entier. Essayez à nouveau.")
    return value


# Définition de la fonction qui vérifie que l'entrée est bien un entier
# Fonction inspirée de la fonction vérifiant les flottants
def get_int_input(signe='all'):
    while True:
        # On vérifie constamment l'entrée
        try:
            # On demande à l'utilisateur d'entrer la valeur
            entree = input("-->")
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



