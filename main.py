""" Ce script permet de générer l'affichage du programme"""
import numpy as np
from verifications import *
from classes import Troncon
from classes import Canalisation
from gestion_BDD_fluides import *
from gestion_BDD_materiaux import *
from gestion_BDD_geometries import *
from gestion_traces import *
from calculs import *

liste_o_n = ['oui', 'non']
# Pour l'instant, on fait que section rondes
liste_sections = ['rond']
liste_materiaux = lister_les_materiaux()
liste_geometrie_angle = ['coude D', 'coude B']
liste_geometries = ['droit'] + liste_geometrie_angle
liste_rap_coude = recuperer_attribut_geo('coude', 'rapport rayon diametre')
rapport_rayon_diam_min = min(liste_rap_coude)
rapport_rayon_diam_max = max(liste_rap_coude)


def choisir_materiaux_canalisation(nbre, choix):
    liste = np.array([])
    if choix == 'non':
        for i in range(nbre):
            print(f"\n Quel est le matériau du tronçon {i} ? Les matériaux possibles sont :")
            afficher_materiaux()
            choix_numeros_materiau = get_element_liste_input([str(i) for i in range(len(liste_materiaux))])
            materiau = liste_materiaux[int(choix_numeros_materiau)]
            liste = np.append(liste, materiau)
    else:
        print(f"\n Quel est le matériau de la canalisation ? Les matériaux possibles sont :")
        afficher_materiaux()
        choix_numeros_materiau = get_element_liste_input([str(a) for a in range(len(liste_materiaux))])
        materiau = liste_materiaux[int(choix_numeros_materiau)]
        for kl in range(nbre):
            liste = np.append(liste, materiau)
    return liste


def choisir_rugosite_canalisation(nbre, choix_rugo, choix_mat, liste_mat):
    liste = []
    # Si la rugosité varie
    if choix_rugo == 'non':
        for j in range(nbre):
            print(f"Connaissez-vous la rugosité du tronçon {j} ?")
            choix_connaitre_rugosite = get_element_liste_input(liste_o_n)
            if choix_connaitre_rugosite == 'oui':
                print(f"\n Quelle est la rugosité du tronçon {j} en m ? Si aucune rugosité, entrez 0.")
                rugosite = get_float_input('+')
                liste = np.append(liste, rugosite)
            else:
                print("La rugosité choisie sera alors celle de la base de données.")
                rugosite = recuperer_rugosite(liste_mat[j]) * 10 ** (-3)
                print(f"Elle vaut {rugosite} m.")
                liste = np.append(liste, rugosite)
    # Si la rugosité est constante
    else:
        # Si le matériau est identique
        if choix_mat == 'oui':
            print(f"Connaissez-vous la rugosité de la canalisation ?")
            choix_connaitre_rugosite = get_element_liste_input(liste_o_n)
            # Si la rugosité est connue
            if choix_connaitre_rugosite == 'oui':
                print(f"\n Quelle est la rugosité de la canalisation en m ? Si aucune rugosité, entrez 0.")
                rugosite = get_float_input('+')
            else:
                print("La rugosité choisie sera alors celle de la base de données.")
                rugosite = recuperer_rugosite(liste_mat[0]) * 10 ** (-3)
                print(f"Elle vaut {rugosite} m.")
        else:
            print(f"\n Quelle est la rugosité de la canalisation en m ? Si aucune rugosité, entrez 0.")
            rugosite = get_float_input('+')

        for lsp in range(nbre):
            liste = np.append(liste, rugosite)
    return liste


def choisir_geometrie_canalisation(nbre):
    liste = []
    for i in range(nbre):
        print(f"\n Quelle est la géométrie du tronçon {i} ?")
        print("'coude D' et 'coude G' correspondent respectivement à un coude qui fait dévier le fluide vers "
              "sa droite et sa gauche.")
        geometrie = get_element_liste_input(liste_geometries)

        # Verification de la possibilité de la configuration
        if i > 0:

            if geometrie in liste_geometrie_angle:
                coude_precedent = liste[0]
                for j in liste:
                    if j in liste_geometrie_angle:
                        coude_precedent = j

                # configurations impossibles
                if coude_precedent == 'coude H':
                    while geometrie == 'coude B':
                        print("Cette configuration n'est pas possible :")
                        print(f"{coude_precedent} ne peut être suivie de {geometrie}")
                        print(f"\n Veuillez entrer à nouveau la géométrie du tronçon {i}.")
                        geometrie = get_element_liste_input(liste_geometries)
                elif coude_precedent == 'coude D':
                    while geometrie == 'coude G':
                        print("Cette configuration n'est pas possible :")
                        print(f"{coude_precedent} ne peut être suivie de {geometrie}")
                        print(f"\n Veuillez entrer à nouveau la géométrie du tronçon {i}.")
                        geometrie = get_element_liste_input(liste_geometries)
                elif coude_precedent == 'coude B':
                    while geometrie == 'coude H':
                        print("Cette configuration n'est pas possible :")
                        print(f"{coude_precedent} ne peut être suivie de {geometrie}")
                        print(f"\n Veuillez entrer à nouveau la géométrie du tronçon {i}.")
                        geometrie = get_element_liste_input(liste_geometries)
                elif coude_precedent == 'coude G':
                    while geometrie == 'coude D':
                        print("Cette configuration n'est pas possible :")
                        print(f"{coude_precedent} ne peut être suivie de {geometrie}")
                        print(f"\n Veuillez entrer à nouveau la géométrie du tronçon {i}.")
                        geometrie = get_element_liste_input(liste_geometries)
                coude_precedent = geometrie
        liste = np.append(liste, geometrie)
    return liste


def choisir_longueur_canalisation(nbre, liste_geo):
    liste_long = []
    liste_rayon = []
    for i in range(nbre):
        geometrie = liste_geo[i]
        if geometrie in liste_geometrie_angle:
            print(f"\n Quel est le rayon de courbure du coude du tronçon {i} en m ?")
            rayon = get_float_input('+')
            liste_long = np.append(liste_long, np.pi*rayon/2)
            liste_rayon = np.append(liste_rayon, rayon)
        else:
            print(f"\n Quelle est la longueur du tronçon {i} en m ?")
            longueur = get_float_input('+')
            liste_long = np.append(liste_long, longueur)
            liste_rayon = np.append(liste_rayon, 0)
    return liste_long, liste_rayon


def verifier_rapport_canalisation(nbre, liste_geo, liste_long, liste_diam, liste_rayon):
    liste = []
    # Vérification du rapport rayon de courbure / diametre
    for i in range(nbre):
        geometrie = liste_geo[i]
        if geometrie in liste_geometrie_angle:
            rayon_courbure = liste_rayon[i]
            diametre = liste_diam[i]
            rapport = rayon_courbure / diametre
            while rapport > rapport_rayon_diam_max or rapport < rapport_rayon_diam_min:
                print(f"\n La base de données ne peut calculer les pertes de charges que pour des rapports rayon de "
                      f"courbure sur diamètre compris entre {rapport_rayon_diam_min} et {rapport_rayon_diam_max}.")
                print(f"Le rapport actuel vaut {rapport}.")
                print(f"Veuillez modifier le rayon de courbure du coude du tronçon {i}, il vaut actuellement {rayon_courbure}.")
                print(f"\n Quel est le rayon du tronçon {i} en m ?")
                rayon_courbure = get_float_input('+')
                rapport = rayon_courbure / diametre
            liste_rayon[i] = rayon_courbure
            liste_long[i] = np.pi*rayon_courbure/2

    return liste_rayon, liste_long


def interface():
    liste_o_n = ['oui','non']
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

        canalisation = Canalisation()

        # Choix matériau
        print("\n Le matériau est-il le même dans toute la canalisation ?")
        choix_materiau = get_element_liste_input(liste_o_n)
        liste_materiau_canalisation = choisir_materiaux_canalisation(nbre_troncons, choix_materiau)

        # Choix rugosité
        print("")
        print("\n La rugosité est-elle la même dans toute la canalisation ?")
        choix_rugosite = get_element_liste_input(liste_o_n)
        liste_rugosite_canalisation = choisir_rugosite_canalisation(nbre_troncons, choix_rugosite, choix_materiau, liste_materiau_canalisation)

        # Choix forme section
        print("\n Quelle est la forme de la section de la canalisation ?")
        forme_section = get_element_liste_input(liste_sections)
        liste_forme_canalisation = [forme_section]*nbre_troncons

        # Choix diamètre
        print("\n Quel est le diamètre de la section de la canalisation en m ?")
        diametre = get_float_input('+')
        liste_diametre_canalisation = [diametre]*nbre_troncons

        # Conditions initiales
        print("\n Quelles sont les conditions initiales du fluides, en entrée de la canalisation ?")
        vitesse_init, temperature_init, pression_init, densite_init, viscosite_init = get_init_cond_input(fluide, diametre)
        liste_pression = [pression_init]
        liste_vitesse = [vitesse_init]
        liste_temperature = [temperature_init]

        # Choix geometrie et angle du tronçon
        liste_geometrie_canalisation = choisir_geometrie_canalisation(nbre_troncons)

        # Choix longueur de chaque tronçon
        liste_longueur_canalisation, liste_rayon_canalisation = choisir_longueur_canalisation(nbre_troncons, liste_geometrie_canalisation)


        liste_rayon_canalisation, liste_longueur_canalisation = verifier_rapport_canalisation(nbre_troncons, liste_geometrie_canalisation, liste_longueur_canalisation, liste_diametre_canalisation, liste_rayon_canalisation)

        # Enregistrement des tronçons et de la canalisation
        for i in range(nbre_troncons):
            longueur = liste_longueur_canalisation[i]
            section = liste_forme_canalisation[i]
            diametre = liste_diametre_canalisation[i]
            materiau = liste_materiau_canalisation[i]
            rugosite = liste_rugosite_canalisation[i]
            geometrie = liste_geometrie_canalisation[i]
            rayon_courbure = liste_rayon_canalisation[i]

            if i == 0:
                vitesse_entree = vitesse_init
                pression_entree = pression_init
                temperature_entree = temperature_init
            else:
                vitesse_entree = 0
                pression_entree = 0
                temperature_entree = 0

            troncon = Troncon(longueur, section, diametre, materiau, rugosite, geometrie, rayon_courbure,
                              fluide, vitesse_entree, pression_entree, temperature_entree, densite_init, viscosite_init)
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
        print("...Tracé de la pression...")
        canalisation.tracer_pression_vitesse_1d()

        # Phase de placement pompe
        print("")
        print("Voulez-vous placer une pompe sur la canalisation ?")
        choix_pompe = get_element_liste_input(liste_o_n)
        if choix_pompe == 'non':
            print("Vous quittez le programme.")
            return True
        else:
            print("Quelle est la valeur de pression sous laquelle il ne faut pas que le fluide descende, en bar ?")
            pression_min = get_float_between_input(0, pression_init)
            print("Quelle est la puissance de votre pompe, en W ?")
            puissance_pompe = get_float_input('+')
            print("Quel est le rendement de votre pompe, entre 0 et 1 ?")
            rendement = get_float_between_input(0, 1)

            liste_pression_discrete, liste_vitesse_discrete, liste_temperature_discrete, liste_abscisse_discrete, liste_longueur = canalisation.calculer_distrib_pression_vitesse()
            liste_debit_discrete = []

            for i in range(len(liste_abscisse_discrete)):
                liste_debit_discrete = np.append(liste_debit_discrete, liste_vitesse_discrete[i]*np.pi*(diametre/2)**2)

            compteur = 0
            pression_entree = liste_pression_discrete[compteur]
            debit = liste_debit_discrete[compteur]
            while compteur < len(liste_pression_discrete) - 1 and pression_entree > pression_min:
                compteur += 1
                pression_entree = liste_pression_discrete[compteur]
                debit = liste_debit_discrete[compteur]

            if compteur == len(liste_pression_discrete):
                print("Le système n'a pas besoin de pompe pour satisfaire les exigences.")
                print("Vous quittez le programme.")
                return True
            else:
                pression_sortie_pompe = calculer_pression_sortie_pompe(puissance_pompe, rendement, debit, pression_entree)

                print(f"Il faut placer une pompe à {liste_abscisse_discrete[compteur]} m.")
                print(f"La pression en sortie sera de {pression_sortie_pompe/10**5} bar.")
                print("Vous quittez le programme.")
                return True



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