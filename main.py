""" Ce script permet de générer l'affichage du programme"""
import numpy as np

from classes import *
from calculs import *
from verifications import *
from gestion_BDD_materiaux import lister_les_materiaux, afficher_materiaux, recuperer_rugosite, ajouter_materiau, supprimer_materiau, modifier_materiau
from gestion_BDD_geometries import recuperer_attribut_geo
from gestion_BDD_fluides import ajouter_fluide, modifier_fluide, supprimer_fluide, afficher_fluide
from gestion_traces import tracer_canalisations, tracer_pression_vitesse_1d
from gestion_YAML import get_name_yaml, get_info_yaml

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
            longueur = rayon*2*np.pi/4  # coude à 90° : 1/4 du périmètre du cercle
        else:
            print(f"\n Quelle est la longueur du tronçon {i} en m ?")
            longueur = get_float_input('+')
            rayon = 0

        liste_long = np.append(liste_long, longueur)
        liste_rayon = np.append(liste_rayon, rayon)

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


def verifier_dans_intervalle(nbre, intervalle):
    a = intervalle[0]
    b = intervalle[1]
    return a < nbre < b


def recuperer_index_plus_proche_inf(liste_abscisse, nbre):
    compteur = 0
    while liste_abscisse[compteur] < nbre:
        compteur += 1
    return compteur


def trouver_emplacement_pompe(liste_pression, pression_min, liste_geometrie, liste_abscisse, liste_longueur):
    compteur = 0
    pression_entree = liste_pression[compteur]
    liste_x_geometrie = np.array([0])

    # On construit la liste des abscisses ou un changement de géométrie a lieu, 0 et la fin en étant
    for idx in range(len(liste_longueur)):
        liste_x_geometrie = np.append(liste_x_geometrie, liste_x_geometrie[-1]+liste_longueur[idx])

    # On construit la liste contenant les abscisses de début et de fin de chaque géométrie
    liste_debut_fin_geo = np.zeros((len(liste_geometrie), 2))
    for i in range(len(liste_geometrie)):
        liste_debut_fin_geo[i][0] = liste_x_geometrie[i]
        liste_debut_fin_geo[i][1] = liste_x_geometrie[i+1]

    # Tant que la pression est au dessus de la pression mini et que le compteur n'est pas à la fin
    while compteur != len(liste_pression) - 1 and pression_entree > pression_min:
        # On actualise le compteur et la pression
        compteur += 1
        pression_entree = liste_pression[compteur]

    # On vérifie que l'abscisse ou la pression min est atteinte n'est pas dans un coude
    abscisse = liste_abscisse[compteur]
    for i in range(len(liste_debut_fin_geo)):
        # Si l'emplacement de la pompe est dans un coude
        if verifier_dans_intervalle(abscisse, liste_debut_fin_geo[i]) and liste_geometrie[i] != 'droit':
            # On renvoie l'index de l'abscisse se situant à l'entrée du coude
            return recuperer_index_plus_proche_inf(liste_abscisse, liste_debut_fin_geo[i][0])

    return compteur


def placer_pompe(debit, liste_abscisse, liste_pression, pression_min, puissance, rendement, liste_geometrie, liste_longueur):

    liste_pression_origine = liste_pression.copy()
    idx_emplacement_pompe = trouver_emplacement_pompe(liste_pression, pression_min, liste_geometrie, liste_abscisse, liste_longueur)

    liste_abscisse_pompe = []
    while idx_emplacement_pompe < len(liste_abscisse) - 1:
        pression_entree = liste_pression[idx_emplacement_pompe]
        pression_sortie_pompe = calculer_pression_sortie_pompe(puissance, rendement, debit, pression_entree)

        print(f"\nIl faut placer une pompe à {liste_abscisse[idx_emplacement_pompe]} m.")
        print(f"La pression en sortie sera de {pression_sortie_pompe / 10 ** 5} bar.")
        delta_pression_pompe = pression_sortie_pompe - liste_pression[idx_emplacement_pompe]
        liste_pression_new = liste_pression[:idx_emplacement_pompe]

        for i in range(idx_emplacement_pompe, len(liste_abscisse)):
            liste_pression_new = np.append(liste_pression_new, liste_pression[i] + delta_pression_pompe)

        liste_abscisse_pompe = np.append(liste_abscisse_pompe, liste_abscisse[idx_emplacement_pompe])

        liste_pression = liste_pression_new.copy()
        idx_emplacement_pompe = trouver_emplacement_pompe(liste_pression, pression_min, liste_geometrie,
                                                          liste_abscisse,
                                                          liste_longueur)

    plt.plot(liste_abscisse, liste_pression_origine, label='Pression originale')
    plt.plot(liste_abscisse, liste_pression_new, label='Pression avec la pompe')
    plt.title("Évolution de la pression le long de la canalisation, en longueur linéaire")
    plt.xlabel("Longueur linéaire en m")
    plt.ylabel("Pression en Pa")
    for idx, i in enumerate(liste_abscisse_pompe):
        plt.axvline(i, color='r', linestyle='--', label=f'Pompe n°{idx+1}')
    plt.legend()
    plt.show()
    return liste_pression_new



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
        print("\n Voulez-vous utiliser un fichier .yaml, celui doit être enregistré dans le même dossier que ce script.")
        choix_yaml = get_element_liste_input(liste_o_n)
        print("Quel est le nom du fichier, suivit de '.yaml'")
        nom_fichier = get_name_yaml()

        if choix_yaml == 'non':
            nettoyer_ecran()
            liste_fluides = lister_fluides()
            print("\n Vous entrez dans le mode de résolution de problème.\n")

            # Fluide
            print("Quel est le fluide s'écoulant dans les canalisations ?")
            fluide = get_element_liste_input(liste_fluides)

            print("\n Combien de tronçons composent la géométrie des canalisations du problème ?")
            nbre_troncons = get_int_input('+')

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
            vitesse_init, temperature_init, pression_init, densite, viscosite_cine, debit = get_init_cond_input(fluide, diametre)
            liste_pression = [pression_init]
            liste_vitesse = [vitesse_init]
            liste_temperature = [temperature_init]

            # Choix geometrie et angle du tronçon
            liste_geometrie_canalisation = choisir_geometrie_canalisation(nbre_troncons)

            # Choix longueur de chaque tronçon
            liste_longueur_canalisation, liste_rayon_canalisation = choisir_longueur_canalisation(nbre_troncons, liste_geometrie_canalisation)

            liste_rayon_canalisation, liste_longueur_canalisation = verifier_rapport_canalisation(nbre_troncons, liste_geometrie_canalisation, liste_longueur_canalisation, liste_diametre_canalisation, liste_rayon_canalisation)

        else:
            fluide, nbre_troncons, materiau, rugosite, forme, diametre, vitesse_init, debit, temperature_init, pression_init, densite, viscosite_cine, liste_geometrie_canalisation, liste_longueur_canalisation, liste_rayon_canalisation, choix_pompe, pression_min, puissance_pompe, rendement = get_info_yaml(nom_fichier)
            pression_init = pression_init * 10**5
            pression_min = pression_min * 10**5

            if vitesse_init == 0:
                vitesse_init = debit / (np.pi*(diametre/2)**2)
            if debit == 0:
                debit = vitesse_init * np.pi*(diametre/2)**2

            for i in range(nbre_troncons):
                longueur = liste_longueur_canalisation[i]
                if longueur == 0:
                    liste_longueur_canalisation[i] = liste_rayon_canalisation[i]*np.pi/2

            liste_forme_canalisation = [forme] * nbre_troncons
            liste_diametre_canalisation = [diametre] * nbre_troncons
            liste_materiau_canalisation = [diametre] * nbre_troncons
            liste_rugosite_canalisation = [rugosite] * nbre_troncons
            # print(liste_longueur_canalisation)
            # print(liste_forme_canalisation)
            # print(liste_diametre_canalisation)
            # print(liste_materiau_canalisation)
            # print(liste_rugosite_canalisation)
            # print(liste_geometrie_canalisation)
            # print(liste_rayon_canalisation)
            # print(pression_init)
            # print(vitesse_init)
            # print(debit)

        canalisation = Canalisation()
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
                              fluide, vitesse_entree, pression_entree, temperature_entree, densite, viscosite_cine)
            canalisation.ajouter_troncon(troncon)

        # Affichage et confirmation de la géométrie des canalisations
            print("La géométrie de votre problème est-elle bien la suivante ?")
            tracer_canalisations(canalisation)
            confirmation_geometrie = get_element_liste_input(['oui', 'non'])

            if confirmation_geometrie == 'non':
                print(f"Pour modifier la canlisation veuillez modifier votre fichier .yaml puis relancer le programme.")
                return True

        # Phase de calculs
        print("...Début de la phase de calculs...")

        liste_pression, liste_vitesse, liste_temperature, liste_abscisse, _ = canalisation.calculer_distrib_pression_vitesse()

        tracer_pression_vitesse_1d(liste_pression, liste_vitesse, liste_abscisse, liste_longueur_canalisation)

        if choix_yaml == 'non':
            # Phase de placement pompe
            print("")
            print("Voulez-vous placer une pompe sur la canalisation ?")
            choix_pompe = get_element_liste_input(liste_o_n)

        if choix_pompe == 'non':
            print("Vous quittez le programme.")
            return True
        else:
            if choix_yaml == 'non':
                print("Quelle est la valeur de pression sous laquelle il ne faut pas que le fluide descende, en bar ?")
                pression_min = get_float_between_input(0, pression_init)*10**5
                print("Quelle est la puissance de votre pompe, en W ?")
                puissance_pompe = get_float_input('+')
                print("Quel est le rendement de votre pompe, entre 0 et 1 ?")
                rendement = get_float_between_input(0, 1)

            placer_pompe(debit, liste_abscisse, liste_pression, pression_min, puissance_pompe, rendement, liste_geometrie_canalisation, liste_longueur_canalisation)

            print("Vous quittez le programme.")
            return True



    # MODE AJOUT/SUPPRESSION DE MATÉRIAU
    elif mode == 2:
        nettoyer_ecran()
        print("\n Voici les matériaux actuels de la base de données")
        afficher_materiaux()
        print("\n Voulez-vous ajouter, modifier ou supprimer un matériau ?")
        choix_edition_2 = get_element_liste_input(['ajouter', 'modifier', 'supprimer'])

        if choix_edition_2 == 'ajouter':
            print("\n Quel est le nom du matériau à ajouter ?")
            nom_materiau = input("--> ")
            print(" Quel est la rugosité du matériau à ajouter ?")
            rugosite_materiau = get_float_input('+')
            ajouter_materiau(nom_materiau, rugosite_materiau)
            print(f"Le matériau '{nom_materiau}' a été ajouté à la base de donnée.")
            print("Vous quittez à présent le programme.")

        elif choix_edition_2 == 'supprimer':
            print("\n Quel est l'index du matériau que vous souhaitez supprimer ?")
            index = get_int_between_input(0, len(lister_les_materiaux()))
            supprimer_materiau(index)
            print(f"Le matériau a été supprimé de la base de données !")
            print("Vous quittez à présent le programme.")

        else:
            print("\n Quel est l'index du matériau que vous souhaitez modifier ? ?")
            index = get_int_between_input(0, len(lister_les_materiaux()))

            print(" Souhaitez-vous modifier le nom du matériau ?")
            if get_element_liste_input(['oui', 'non']) == 'oui':
                new_nom_materiau = input("--> ")
                modifier_materiau(index, new_nom_materiau, rugosite=None)

            print(" Souhaitez-vous modifier la rugosité du matériau ?")
            if get_element_liste_input(['oui', 'non']) == 'oui':
                new_rugosite_materiau = get_float_input('+')
                modifier_materiau(index, materiau=None, new_rugosite_materiau)

            print("\n Le matériau a été modifié !")
            print("Vous quittez à présent le programme.")

    # MODE AJOUT/SUPPRESSION DE FLUIDE
    elif mode == 3:
        nettoyer_ecran()
        print("\n Voici les fluides actuels de la base de données")
        afficher_fluide()
        print("\n Voulez-vous ajouter, modifier ou supprimer un fluide ?")
        choix_edition_3 = get_element_liste_input(['ajouter', 'modifier', 'supprimer'])

        if choix_edition_3 == 'ajouter':
            print("\n Quel est le nom du fluide à ajouter ?")
            nom = input("--> ")

            print(" Quel est la température du fluide à ajouter ?")
            temperature = get_float_input('+')

            print("\n Quel est la masse volumique du fluide à ajouter, en kg/m3 ?")
            densite = get_float_input('+')

            print("\n Quel est la viscosité cinématique du fluide à ajouter ?")
            viscosite_cin = get_float_input('+')

            print(" Quel est la viscosité dynamique du fluide à ajouter ?")
            viscosite_dyn = get_float_input('+')

            print(" Quel est la chaleur massique du fluide à ajouter ?")
            chaleur = get_float_input('+')

            print(" Quel est la conductivité du fluide à ajouter ?")
            conductivite = get_float_input('+')

            print(" Quel est le coefficient de dilatation du fluide à ajouter ?")
            coef_dil = get_float_input('+')

            ajouter_fluide(nom, temperature, densite, viscosite_dyn, viscosite_cin, chaleur, conductivite, coef_dil)
            print(f"Le fluide '{nom}' a été ajouté à la base de donnée.")
            print("Vous quittez à présent le programme.")

        elif choix_edition_3 == 'supprimer':
            print("\n Quel est l'index du fluide que vous souhaitez supprimer ?")
            index = get_int_between_input(0, len(lister_fluides()))
            supprimer_fluide(index)
            print(f"Le fluide a été supprimé de la base de données !")
            print("Vous quittez à présent le programme.")

        else:
            print("\n Quel est l'index du fluide que vous souhaitez modifier ? ?")
            index = get_int_between_input(0, len(lister_fluides()))

            print("\n Souhaitez-vous modifier le nom du fluide ?")
            if get_element_liste_input(['oui', 'non']) == 'oui':
                print("Quel est le nouveau nom du fluide ?")
                new_nom_fluide = input("--> ")
                modifier_fluide(index, new_nom_fluide, temperature=None, masse_volumique=None, viscosite_dynamique=None,
                                viscosite_cinematique=None, chaleur_massique=None,
                                conductivite_thermique=None, coefficient_dilatation=None)

            print("\n Souhaitez-vous modifier la température du fluide ?")
            if get_element_liste_input(['oui', 'non']) == 'oui':
                print("Quelle est la nouvelle température du fluide, en °C ?")
                temperature = get_float_input('+')
                modifier_fluide(index, temperature, nom_fluide=None, masse_volumique=None, viscosite_dynamique=None,
                                viscosite_cinematique=None, chaleur_massique=None, conductivite_thermique=None,
                                coefficient_dilatation=None)

            print("\n Souhaitez-vous modifier la masse volumique du fluide ?")
            if get_element_liste_input(['oui', 'non']) == 'oui':
                print("Quelle est la nouvelle masse volumique du fluide, kg/m3 ?")
                densite = get_float_input('+')
                modifier_fluide(index, densite, nom_fluide=None, temperature=None, viscosite_dynamique=None,
                                viscosite_cinematique=None, chaleur_massique=None, conductivite_thermique=None,
                                coefficient_dilatation=None)

            print("\n Souhaitez-vous modifier la viscosité cinématique du fluide ?")
            if get_element_liste_input(['oui', 'non']) == 'oui':
                print("Quelle est la nouvelle viscosité cinématique du fluide, en m2/s ?")
                viscosite_cin = get_float_input('+')
                modifier_fluide(index, viscosite_cin, nom_fluide=None, temperature=None, masse_volumique=None, viscosite_dynamique=None,
                                chaleur_massique=None, conductivite_thermique=None,
                                coefficient_dilatation=None)

            print("\n Souhaitez-vous modifier la viscosité dynamique du fluide ?")
            if get_element_liste_input(['oui', 'non']) == 'oui':
                print("Quelle est la nouvelle viscosité dynamique du fluide, en Pa.s ?")
                viscosite_dyn = get_float_input('+')
                modifier_fluide(index, viscosite_dyn, nom_fluide=None, temperature=None, masse_volumique=None,
                                viscosite_cinematique=None, chaleur_massique=None, conductivite_thermique=None,
                                coefficient_dilatation=None)

            print("\n Souhaitez-vous modifier la chaleur massique du fluide ?")
            if get_element_liste_input(['oui', 'non']) == 'oui':
                print("Quelle est la nouvelle chaleur massique du fluide, J/(kg.K) ?")
                chaleur = get_float_input('+')
                modifier_fluide(index, chaleur, nom_fluide=None, temperature=None, masse_volumique=None, viscosite_dynamique=None,
                                viscosite_cinematique=None, conductivite_thermique=None,
                                coefficient_dilatation=None)

            print("\n Souhaitez-vous modifier la conductivité du fluide ?")
            if get_element_liste_input(['oui', 'non']) == 'oui':
                print("Quelle est la nouvelle conductivité du fluide, en W/(m·K) ?")
                conductivite = get_float_input('+')
                modifier_fluide(index, conductivite, nom_fluide=None, temperature=None, masse_volumique=None, viscosite_dynamique=None,
                                viscosite_cinematique=None, chaleur_massique=None,
                                coefficient_dilatation=None)

            print("\n Souhaitez-vous modifier le coefficient de dilatation du fluide ?")
            if get_element_liste_input(['oui', 'non']) == 'oui':
                print("Quel est le nouveau coefficient de dilatation du fluide, en /K ?")
                coef_dilat = get_float_input('+')
                modifier_fluide(index, coefficient_dilat, nom_fluide=None, temperature=None, masse_volumique=None, viscosite_dynamique=None,
                                viscosite_cinematique=None, chaleur_massique=None, conductivite_thermique=None)

            print(f"Le fluide a été modifié !")
            print("Vous quittez à présent le programme.")

            print(" Souhaitez-vous modifier le nom du matériau ?")
            if get_element_liste_input(['oui', 'non']) == 'oui':
                new_nom_materiau = input("--> ")
                modifier_materiau(index, new_nom_materiau, rugosite=None)

            print(" Souhaitez-vous modifier la rugosité du matériau ?")
            if get_element_liste_input(['oui', 'non']) == 'oui':
                new_rugosite_materiau = get_float_input('+')
                modifier_materiau(index, materiau=None, new_rugosite_materiau)

            print("\n Le matériau a été modifié !")
            print("Vous quittez à présent le programme.")


if __name__ == '__main__':
    interface()
    # liste_pression = np.append(np.linspace(3, 2.9, 200), np.linspace(2.9, 2.5, 157)[1:])
    # pression_min = 2.7
    # liste_geometrie = ['droit', 'coude D', 'droit']
    # liste_abscisse = np.append(np.linspace(0, 2, 200), np.linspace(2, 3.57, 157)[1:])
    # liste_longueur = [2, 1.57, 5]
    # print(trouver_emplacement_pompe(liste_pression, pression_min, liste_geometrie, liste_abscisse, liste_longueur))
