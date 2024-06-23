""" Ce script permet de générer l'affichage du programme"""
import numpy as np
from verifications import *
from classes import *
from GestionBDDFluide import *
from GestionBDDMateriau import *


def interface():
    nettoyer_ecran()

    # Affichage du principe du script
    print("Ce script permet de configurer des canalisations ! \n"
          "En entrant différentes données de votre problème : géométrie, conditions initiales, fluide, ... \n"
          "Le script sera en mesure de vous afficher les variations de pression, vitesse, contrainte. \n"
          "Ainsi il vous indiquera ou placer des pompes par exemple.\n \n"
          "Pour commencer il faut découper la géométrie des canalisations en tronçons ! \n"
          "Un tronçon est une partie de la géométrie dont la section, la direction ou le matériau ne varie pas. \n")

    # Choix du mode de fonctionnement
    # 1 - normal, 2 - ajout de matériau, 3 - ajout de fluide
    mode = get_choix_mode()

    # MODE PROBLÈME
    if mode == 1:
        print("\n Vous entrez dans le mode de résolution de problème.")
        print("Combien de sections composent la géométrie des canalisations du problème ?")
        nbre_troncons = get_int_input('+')
        liste_troncons = np.zeros(nbre_troncons)
        liste_section = ['carré', 'rond']
        liste_materiau = ['PVC', 'bois', 'béton']
        liste_geometrie = ['droit', 'coude', 'T']
        liste_geometrie_angle = ['coude', 'T']
        angle = 180  # Par défaut, l'angle du tronçon vaut 180°, portion droite

        for i in range(nbre_troncons):
            # Définition du tronçon
            troncon = Troncon()

            # Longueur du tronçon
            print(f"Quelle est la longueur du tronçon {i} ? \n")
            longueur = get_float_input('+')
            troncon.ajouter_attribut(longueur)

            # Forme de la section du tronçon
            print(f"Quelle est la forme de la section du tronçon {i} ? \n")
            section = get_element_liste_input(liste_section)
            troncon.ajouter_attribut(section)

            # Diamètre/largeur du tronçon
            print(f"Quelle est le diamètre/largeur de la section du tronçon {i} ? \n")
            diametre = get_float_input('+')
            troncon.ajouter_attribut(diametre)

            # Matériau du tronçon
            print(f"Quelle est le matériau de la section du tronçon {i} ? \n")
            materiau = get_element_liste_input(liste_materiau)
            troncon.ajouter_attribut(materiau)

            # Rugosité du tronçon
            print(f"Quelle est la rugosité de la section du tronçon {i} ? \n")
            rugosite = get_float_input('+')
            troncon.ajouter_attribut(rugosite)

            # Forme et angle du tronçon
            print(f"Quelle est la géométrie de la section du tronçon {i} ? \n")
            geometrie = get_element_liste_input(liste_geometrie)
            troncon.ajouter_attribut(geometrie)

            if geometrie in liste_geometrie_angle:
                print(f"Quelle est l'angle du {geometrie} en ° ? \n")
                angle = get_float_input()
            troncon.ajouter_attribut(angle)

            # Enregistrement de tous les tronçons les données
            liste_troncons = np.append(liste_troncons, troncon)

            # Début des calculs

    # MODE AJOUT/SUPPRESSION DE MATÉRIAU
    elif mode == 2:
        print("Voici les matériaux actuels de la base de données")
        afficher_materiaux()
        print("\n Voulez-vous ajouter ou supprimer un matériau.")
        get_element_liste_input(['ajouter', 'supprimer'])

    # MODE AJOUT/SUPPRESSION DE FLUIDE
    else:
        print("Voici les matériaux actuels de la base de données")
        afficher_fluide()
        print("\n Voulez-vous ajouter ou supprimer un matériau.")
        get_element_liste_input(['ajouter', 'supprimer'])






interface()