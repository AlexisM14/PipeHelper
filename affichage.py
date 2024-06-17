""" Ce script permet de générer l'affichage du programme"""
import numpy as np
from verifications import *
from classes import *


def interface():
    nettoyer_ecran()

    print("Ce script permet de configurer des canalisations ! \n"
          "En entrant différentes données de votre problème : géométrie, conditions initiales, fluide, ... \n"
          "Le script sera en mesure de vous afficher les variations de pression, vitesse, contrainte. \n"
          "Ainsi il vous indiquera ou placer des pompes par exemple.\n \n"
          "Pour commencer il faut découper la géométrie des canalisations en tronçons ! \n"
          "Un tronçon est une partie de la géométrie dont la section, la direction ou le matériau ne varie pas. \n")

    print("Combien de sections composent la géométrie des canalisations du problème ?")
    nbre_troncons = get_int_input('+')
    liste_troncons = np.zeros(nbre_troncons)

    for i in range(nbre_troncons):
        print(f"Quelle est la longueur du tronçon {i} ? \n")
        longueur = get_float_input('+')
        print(f"Quelle est la forme de la section du tronçon {i} ? \n")
        section = get_branch_input()
        print(f"Quelle est le diamètre de la section du tronçon {i} ? \n")
        diametre = get_float_input('+')
        print(f"Quelle est le matériau de la section du tronçon {i} ? \n")
        materiau = get_mat_input()
        print(f"Quelle est la rugosité de la section du tronçon {i} ? \n")
        rugosite = get_float_input('+')
        troncon = Troncon(longueur, section, diametre, materiau, rugosite)
        liste_troncons = np.append(liste_troncons, troncon)






interface()