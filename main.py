""" Ce script permet de générer l'affichage du programme"""
import numpy as np
from verifications import *
from classes import Troncon
from classes import Canalisation
from gestion_BDD_fluides import *
from gestion_BDD_materiaux import *
from gestion_BDD_geometries import *


def interface():

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
        nettoyer_ecran()
        liste_fluides = lister_fluides()
        print("\n Vous entrez dans le mode de résolution de problème.\n")

        # Fluide
        print("Quel est le fluide s'écoulant dans les canalisations ?")
        fluide = get_element_liste_input(liste_fluides)

        print("\n Combien de sections composent la géométrie des canalisations du problème ?")
        nbre_troncons = get_int_input('+')
        liste_troncons = np.zeros(nbre_troncons)
        # Pour l'instant on fait que section rondes
        liste_sections = ['rond']
        liste_materiaux = ['PVC', 'bois', 'béton']
        # liste_materiaux = lister_les_materiaux()
        liste_geometries = ['droit', 'coude D', 'coude B' 'coude G', 'coude H']
        liste_geometrie_angle = ['coude D', 'coude B' 'coude G', 'coude H']

        canalisation = Canalisation()

        for i in range(nbre_troncons):
            # Longueur du tronçon
            print(f"\n Quelle est la longueur du tronçon {i} en m ?")
            longueur = get_float_input('+')

            # Forme de la section du tronçon
            print(f"\n Quelle est la forme de la section du tronçon {i} ?")
            section = get_element_liste_input(liste_sections)

            # Diamètre/largeur du tronçon
            print(f"\n Quelle est le diamètre de la section du tronçon {i} en m ?")
            diametre = get_float_input('+')

            # Matériau du tronçon
            print(f"\n Quelle est le matériau de la section du tronçon {i} ?")
            materiau = get_element_liste_input(liste_materiaux)

            # Rugosité du tronçon
            print(f"\n Quelle est la rugosité de la section du tronçon {i} en m ?")
            rugosite = get_float_input('+')

            # Forme et angle du tronçon
            print(f"\n Quelle est la géométrie de la section du tronçon {i} ?")
            print("'coude D' et 'coude G' correspondent respectivement à un coude qui part vers "
                  "la droite et la gauche. \n De mâme, 'coude H' et 'coude B' correspondent respectivement à un "
                  "coude qui part vers le haut et vers le bas. \n Ces direction étant par rapport à la direction "
                  "initiale du fluide. ")
            geometrie = get_element_liste_input(liste_geometries)

            # Rayon de courbure du tronçon
            rayon_courbure = 0
            if geometrie[:-2] == 'coude':
                liste_rap_coude = recuperer_attribut_geo('coude', 'rapport rayon diametre')
                print(f"\n Quel est le rayon de courbure du {geometrie} du tronçon {i} en m ?")
                rayon_courbure = get_float_input('+')
                rapport_rayon_diam_min = min(liste_rap_coude)
                rapport_rayon_diam_max = max(liste_rap_coude)
                while (rayon_courbure / diametre) > rapport_rayon_diam_max or (rayon_courbure/diametre) < rapport_rayon_diam_min:
                    print(f"Le rapport rayon de courbure doit être compris entre {rapport_rayon_diam_min} et {rapport_rayon_diam_max}.")
                    print(f"Le rapport actuel vaut {rayon_courbure/diametre}.")
                    print("Voulez-vous modifier le rayon de courbure ou le diamètre du tronçon ?")
                    choix_modif = get_element_liste_input(['rayon de courbure', 'diamètre'])
                    if choix_modif == 'rayon de courbure':
                        print(f"\n Quel est le rayon de courbure du {geometrie} du tronçon {i} en m ?")
                        rayon_courbure = get_float_input('+')
                    else:
                        print(f"\n Quelle est le diamètre de la section du tronçon {i} en m ? \n")
                        diametre = get_float_input('+')

            angle = 0  # Par défaut, l'angle du tronçon vaut 0°, portion droite. Un coude vaut 90°
            if geometrie in liste_geometrie_angle:
                angle = 90

            vitesse_init = 0
            temperature_init = 0
            pression_init = 0
            # Condition initiales
            if i == 0:
                print("\n Quelles sont les conditions initiales du fluides, en entrée de la canalisation ?")
                vitesse_init, temperature_init, pression_init = get_init_cond_input()
                liste_temperature = recuperer_liste_temperature(fluide)
                if temperature_init < min(liste_temperature) or temperature_init > max(liste_temperature):
                    print(f"La température initiale doit être comprise entre {min(liste_temperature)} °C et {max(liste_temperature)} °C ")
                    print(f"La température initiale actuelle vaut {temperature_init} °C, veuillez la modifier.")
                    temperature_init = get_float_input('+')

            # On enregistre toutes les valeurs dans un tronçon
            troncon = Troncon(longueur, section, diametre, materiau, rugosite, geometrie, angle, rayon_courbure, fluide, vitesse_init, pression_init, temperature_init)
            # On enregistre le tronçon dans la canalisation
            canalisation.ajouter_troncon(troncon)

        # Affichage de la géométrie des canalisations
        print(f"longueur : {canalisation.renvoyer_liste_longueur()}")
        print(f"géométrie : {canalisation.renvoyer_liste_geometrie()}")

        # Début des calculs

    # MODE AJOUT/SUPPRESSION DE MATÉRIAU
    elif mode == 2:
        nettoyer_ecran()
        print("Non disponible pour l'instant, veuillez entrer dans le mode normal.")
        print("")
        interface()
        return True
        # print("Voici les matériaux actuels de la base de données")
        # afficher_materiaux()
        # print("\n Voulez-vous ajouter ou supprimer un matériau.")
        # choix_edition_2 = get_element_liste_input(['ajouter', 'supprimer'])
        #
        # if choix_edition_2 == 'ajouter':
        #     ajouter_materiaux()
        # else:
        #     supprimer_materiaux()

    # MODE AJOUT/SUPPRESSION DE FLUIDE
    elif mode == 3:
        nettoyer_ecran()
        print("Non disponible pour l'instant, veuillez entrer dans le mode normal.")
        print("")
        interface()
        return True
        # print("Voici les matériaux actuels de la base de données")
        # afficher_fluide()
        # print("\n Voulez-vous ajouter ou supprimer un matériau.")
        # choix_edition_3 = get_element_liste_input(['ajouter', 'supprimer'])
        #
        # if choix_edition_3 == 'ajouter':
        #     ajouter_fluides()
        # else:
        #     supprimer_fluides()

interface()