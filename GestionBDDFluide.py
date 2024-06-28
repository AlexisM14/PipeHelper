from verifications import *

# On utilise une base de données pour des fluides à TPN


def afficher_fluide():
    """Affiche les différents fluides de la base de données"""
    return True


def lister_les_fluides():
    return True


def ajouter_densite(nom_fluide, temperature):
    """Permet d'ajouter une densité au fluide dans la base de données pour une certaine température"""
    return True


def ajouter_viscosite(nom_fluide, temperature):
    """Permet d'ajouter une viscosité au fluide dans la base de données pour une certaine température"""
    return True


def ajouter_fluides():
    """Permet d'ajouter un fluide à la base de données"""
    nom_fluide = input("Quel est le nom du fluide que vous voulez ajouter la base de données ?")
    print("Quelle est la température du fluide que vous voulez ajouter, en K ?")
    temperature = get_float_input()
    reponse = 'non'
    while reponse == 'non':
        print(f"Vous voulez ajouter les propriétés du {nom_fluide} à {temperature} K ?")
        reponse = get_element_liste_input(['oui', 'non'])
        nom_fluide = input("Quel est le nom du fluide que vous voulez ajouter la base de données ?")
        print("Quelle est la température du fluide que vous voulez ajouter ?")
        temperature = get_float_input()

    # On ajoute le nom et la température à la base de données puis la densité et la viscosité

    ajouter_densite(nom_fluide, temperature)
    ajouter_viscosite(nom_fluide, temperature)
    return True


def recuperer_densite(nom_fluide, temperature):
    return 23,4


def modifier_densite(nom_fluide, temperature):
    """Permet de modifier une densité au fluide dans la base de données pour une certaine température"""
    densite = recuperer_densite(nom_fluide, temperature)
    print(f"La densité actuelle pour {nom_fluide} à {temperature} K est {densite} kg/m3, voulez vous la modifier ?")
    reponse = get_element_liste_input(['oui', 'non'])
    if reponse == 'oui':
        print("Entrez la nouvelle densité en kg/m3")
        nouvelle_densite = get_float_input('+')
        print(f"La nouvelle densité sera donc {nouvelle_densite} kg/m3 ?")
        confirmation = 'non'
        while confirmation == 'non':
            print("Entrez la nouvelle densité en kg/m3")
            nouvelle_densite = get_float_input('+')
            print(f"La nouvelle densité sera donc {nouvelle_densite} kg/m3 ?")
            confirmation = get_element_liste_input(['oui', 'non'])
        # on modifie la densite
    else:
        print(f"Vous sortez de la modification de la densité de {nom_fluide} à {temperature} K")


def modifier_viscosite(nom_fluide, temperature):
    """Permet de modifier une viscosité au fluide dans la base de données pour une certaine température"""
    viscosite = recuperer_densite(nom_fluide, temperature)
    print(f"La viscosité actuelle pour {nom_fluide} à {temperature} K est {viscosite} Pa.s, voulez vous la modifier ?")
    reponse = get_element_liste_input(['oui', 'non'])
    if reponse == 'oui':
        print("Entrez la nouvelle viscosité en Pa.s")
        nouvelle_viscosite = get_float_input('+')
        print(f"La nouvelle viscosité sera donc {nouvelle_viscosite} Pa.s ?")
        confirmation = 'non'
        while confirmation == 'non':
            print("Entrez la nouvelle viscosité en Pa.s")
            nouvelle_viscosite = get_float_input('+')
            print(f"La nouvelle viscosité sera donc {nouvelle_viscosite} Pa.s ?")
            confirmation = get_element_liste_input(['oui', 'non'])
        # on modifie la viscosite
    else:
        print(f"Vous sortez de la modification de la viscosité de {nom_fluide} à {temperature} K")


def supprimer_fluides():
    """Permet de supprimer un fluide de la base de données"""
    return True