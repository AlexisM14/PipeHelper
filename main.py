""" Ce script permet de générer l'affichage du programme"""
import numpy as np
from verifications import *
from classes import Troncon
from classes import Canalisation
from gestion_BDD_fluides import *
from gestion_BDD_materiaux import *
from gestion_BDD_geometries import *
from gestion_traces import *


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

        print("\n Combien de tronçons composent la géométrie des canalisations du problème ?")
        nbre_troncons = get_int_input('+')
        liste_troncons = np.zeros(nbre_troncons)
        # Pour l'instant on fait que section rondes
        liste_sections = ['rond']
        liste_materiaux = lister_les_materiaux()
        liste_geometries = ['droit', 'coude D', 'coude B' 'coude G', 'coude H']
        liste_geometrie_angle = ['coude D', 'coude B' 'coude G', 'coude H']

        print("\n Quelles sont les conditions initiales du fluides, en entrée de la canalisation ?")
        vitesse_init, temperature_init, pression_init = get_init_cond_input()
        liste_temperature = recuperer_liste_temperature(fluide)
        if temperature_init < min(liste_temperature) or temperature_init > max(liste_temperature):
            print(
                f"La température initiale doit être comprise entre {min(liste_temperature)} °C et {max(liste_temperature)} °C ")
            print(f"La température initiale actuelle vaut {temperature_init} °C, veuillez la modifier.")
            temperature_init = get_float_input('+')
        liste_pression = [pression_init]
        liste_vitesse = [vitesse_init]
        liste_temperature = [temperature_init]

        canalisation = Canalisation()

        for i in range(nbre_troncons):

            # Conditions initiales
            vitesse = 0
            temperature = 0
            pression = 0

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
            print(f"\n Quelle est le matériau du tronçon {i} ? Les matériaux possibles sont :")
            afficher_materiaux()
            choix_numeros_materiau = get_element_liste_input([str(i) for i in range(len(liste_materiaux))])
            materiau = liste_materiaux[int(choix_numeros_materiau)]

            # Rugosité du tronçon
            print(f"Connaissez-vous la rugosité du tronçon {i} ?")
            choix_rugosite = get_element_liste_input(['oui','non'])
            if choix_rugosite == 'oui':
                print(f"\n Quelle est la rugosité de la section du tronçon {i} en m ?")
                rugosite = get_float_input('+')
            else:
                print("La rugosité sera alors prise dans la base de données.")
                rugosite = recuperer_rugosite(materiau)*10**(-3)
                print(f"Elle vaut {rugosite} m")
            # Forme et angle du tronçon
            print(f"\n Quelle est la géométrie de la section du tronçon {i} ?")
            print("'coude D' et 'coude G' correspondent respectivement à un coude qui part vers "
                  "la droite et la gauche. \n De mâme, 'coude H' et 'coude B' correspondent respectivement à un "
                  "coude qui part vers le haut et vers le bas. \n Ces direction étant par rapport à la direction "
                  "initiale du fluide. ")
            geometrie = get_element_liste_input(liste_geometries)

            angle = 0  # Par défaut, l'angle du tronçon vaut 0°, portion droite. Un coude vaut 90°
            if geometrie in liste_geometrie_angle:
                angle = 90

            # Rayon de courbure du tronçon
            rayon_courbure = 0
            if geometrie.split(' ')[0] == 'coude':
                liste_rap_coude = recuperer_attribut_geo('coude', 'rapport rayon diametre')
                rayon_courbure = longueur / np.deg2rad(angle)
                rapport_rayon_diam_min = min(liste_rap_coude)
                rapport_rayon_diam_max = max(liste_rap_coude)
                while (rayon_courbure / diametre) > rapport_rayon_diam_max or (rayon_courbure/diametre) < rapport_rayon_diam_min:
                    print(f"Le rapport rayon de courbure doit être compris entre {rapport_rayon_diam_min} et {rapport_rayon_diam_max}.")
                    print(f"Le rapport actuel vaut {rayon_courbure/diametre}.")
                    print("Voulez-vous modifier la longueur du tronçon ou le diamètre du tronçon ?")
                    choix_modif = get_element_liste_input(['longueur', 'diamètre'])
                    if choix_modif == 'longueur':
                        print(f"\n Quel est la longueur du {geometrie} du tronçon {i} en m ?")
                        longueur = get_float_input('+')
                    else:
                        print(f"\n Quelle est le diamètre de la section du tronçon {i} en m ? \n")
                        diametre = get_float_input('+')
                    rayon_courbure = longueur / np.deg2rad(angle)

            # On enregistre toutes les valeurs dans un tronçon
            if i == 0:
                troncon = Troncon(longueur, section, diametre, materiau, rugosite, geometrie, angle, rayon_courbure, fluide, vitesse_init, pression_init, temperature_init)

            troncon = Troncon(longueur, section, diametre, materiau, rugosite, geometrie, angle, rayon_courbure, fluide, vitesse, pression, temperature)
            # On enregistre le tronçon dans la canalisation
            canalisation.ajouter_troncon(troncon)

        # Affichage de la géométrie des canalisations
        print("La géométrie de votre problème est-elle bien la suivante ?")
        tracer_canalisations(canalisation)
        confirmation_geometrie = get_element_liste_input(['oui', 'non'])
        if confirmation_geometrie == 'non':
            print("Il n'est pas disponible de modifier la géométrie du problème pour l'instant")
            print("voulez-vous recommencer depuis le début ? ")
            choix_recommencer = get_element_liste_input(['oui', 'non'])
            if choix_recommencer == 'oui':
                interface()
                return True

        # Phase de calculs
        print("...Début de la phase de calculs...")
        liste_longueur = [0] + canalisation.renvoyer_liste_longueur()
        longueur_totale = sum(liste_longueur)

        for i in range(nbre_troncons):
            troncon = canalisation.renvoyer_troncon(i)
            pression_entree = liste_pression[i]

            # Si la vitesse en entrée ou la pression en entrée est nulle alors elle restera nulle
            # car aucune action de gravité
            if pression_entree == 0 or liste_vitesse[-1]:
                liste_pression = np.append(liste_pression, 0)
                liste_vitesse = np.append(liste_vitesse, 0)
            else:
                # Calcul des pertes de charges et pression de sortie
                delta_reguliere = troncon.calculer_delta_pression_reguliere_troncon()
                delta_singuliere = troncon.calculer_delta_pression_singuliere_troncon()
                delta_pression = delta_singuliere + delta_reguliere
                pression_sortie = pression_entree - delta_pression

                # Calcul de la vitesse de sortie
                densite = troncon.recuperer_densite()
                coef_singuliere = troncon.calculer_coef_singuliere_troncon()
                vitesse_entree = liste_vitesse[-1]
                vitesse_sortie = calculer_vitesse_sortie(vitesse_entree, pression_entree, pression_sortie, delta_reguliere, densite, coef_singuliere)

                # Si les pressions et vitesses calculées sont négatives alors on dit qu'elles sont nulles car
                # elle ne peuvent pas devenir négative dans de telles conditions
                if vitesse_sortie > 0:
                    liste_vitesse = np.append(liste_vitesse, vitesse_sortie)
                if pression_sortie > 0:
                    liste_pression = np.append(liste_pression, pression_sortie)
                liste_pression = np.append(liste_pression, 0)
                liste_vitesse = np.append(liste_vitesse, 0)

        # On trace la variation de pression et de vitesse
        tracer_pression_1d(liste_pression, liste_longueur)
        tracer_vitesse_1d(liste_vitesse, liste_longueur)

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