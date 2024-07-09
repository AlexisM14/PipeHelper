"""
File: gestion_traces.py
Author: Alexis Markiewicz
Date: 2024-07-08
Description: Ce script permet de définir des fonctions qui tracerons les variations de pressions et la géométrie d'une canalisation
"""

# Imports
import numpy as np
import matplotlib.pyplot as plt
from classes import Troncon, Canalisation


# La direction x va de gauche à droite, 'x+' va vers la droite
# La direction y va de haut en bas, 'y+' va vers le haut


# Définitions des fonctions
def calculer_coordonnees_coude(x_debut, y_debut, rayon, angle_deg, orientation, direction):
    """Cette fonction permet de calculer les coordonnées d'un coude.

    :param x_debut: La coordonnée x ou démarre le coude
    :type x_debut: float
    :param y_debut: La coordonnée y ou démarre le coude
    :type y_debut: float
    :param rayon: Le rayon de courbure du coude
    :type rayon: float
    :param angle_deg: L'angle du coude, en °
    :type angle_deg: float
    :param orientation: Le sens dans lequel le fluide est dirigé ('G' ou 'D')
    :type orientation: str
    :param direction: La direction d'ou vient le fluide ('x+' : le fluide va dans le sens des x croissant,
    'x-' : Le fluide va dans le sens des x décroissant, idem pour 'y+' et 'y-')
    :type direction: str

    :return: La liste des coordonnées x du coude
    :rtype: list
    :return: La liste des coordonnées y du coude
    :rtype: list
    """
    # Conversion de l'angle en radian
    angle_rad = np.radians(angle_deg)

    longueur = np.pi * rayon / 2

    nbre_points = int(longueur * 100)

    # Liste des angles balayés
    angles = np.linspace(0, angle_rad, nbre_points)

    x = np.zeros(nbre_points)
    y = np.zeros(nbre_points)

    # Si le fluide va vers sa droite
    if orientation == 'D':
        if direction == 'x-':
            for i in range(nbre_points):
                x[i] = x_debut + rayon * (-np.cos(angles[i]))
                y[i] = y_debut + rayon * (1 - np.sin(angles[i]))
            x = np.flip(x)
            y = np.flip(y)

        if direction == 'x+':
            for i in range(nbre_points):
                x[i] = x_debut + rayon * (np.cos(angles[i]))
                y[i] = y_debut + rayon * (np.sin(angles[i]) - 1)
            x = np.flip(x)
            y = np.flip(y)

        if direction == 'y+':
            for i in range(nbre_points):
                x[i] = x_debut + rayon * (1 - np.cos(angles[i]))
                y[i] = y_debut + rayon * (np.sin(angles[i]))

        if direction == 'y-':
            for i in range(nbre_points):
                x[i] = x_debut + rayon * (np.cos(angles[i])-1)
                y[i] = y_debut + rayon * (-np.sin(angles[i]))

    # Si le fluide va vers sa gauche
    elif orientation == 'G':
        if direction == 'x+':
            for i in range(nbre_points):
                x[i] = x_debut + rayon * (np.cos(angles[i]))
                y[i] = y_debut + rayon * (1 - np.sin(angles[i]))
            x = np.flip(x)
            y = np.flip(y)

        if direction == 'x-':
            for i in range(nbre_points):
                x[i] = x_debut + rayon * (-np.cos(angles[i]))
                y[i] = y_debut + rayon * (np.sin(angles[i])-1)
            x = np.flip(x)
            y = np.flip(y)

        if direction == 'y-':
            for i in range(nbre_points):
                x[i] = x_debut + rayon * (1-np.cos(angles[i]))
                y[i] = y_debut + rayon * (- np.sin(angles[i]))

        if direction == 'y+':
            for i in range(nbre_points):
                x[i] = x_debut + rayon * (np.cos(angles[i])-1)
                y[i] = y_debut + rayon * (np.sin(angles[i]))

    return x, y


def calculer_coordonnees_guide(canalisation, x_debut, y_debut, direction='y+'):
    """Cette fonction permet de calculer les coordonnées d'une canalisation.

    :param canalisation: La canalisation étudiée
    :type canalisation: Canalisatiobn
    :param x_debut: La coordonnée x ou démarre le coude
    :type x_debut: Canalisatiobn
    :param y_debut: La coordonnée y ou démarre le coude
    :type y_debut: Canalisatiobn
    :param direction: La direction d'ou vient le fluide ('x+' : le fluide va dans le sens des x croissant, 'x-' : Le fluide va dans le sens des x décroissant, idem pour 'y+' et 'y-'), optionnel
    :type direction: Canalisatiobn

    :return: La liste des coordonnées x de la canalisation
    :rtype: list
    :return: La liste des coordonnées y de la canalisation
    :rtype: list
    """
    # On récupère les longueurs, géométries, rayons et le nombre de tronçons de la canalisation
    liste_longueur = canalisation.renvoyer_liste_longueur()
    liste_geometrie = canalisation.renvoyer_liste_geometrie()
    nbre_troncons = canalisation.recupere_nbre_troncons()
    liste_rayon = canalisation.renvoyer_liste_courbure()

    x = np.array([x_debut])
    y = np.array([y_debut])

    for i in range(nbre_troncons):
        nbre_points = int(liste_longueur[i] * 100)

        increment = float(liste_longueur[i]) / nbre_points

        # Si le tronçon est droit
        if liste_geometrie[i] == 'droit':
            if direction == 'y+':
                for j in range(nbre_points):
                    x = np.append(x, x[-1] * nbre_points)
                    y = np.append(y, y[-1] + increment)

            elif direction == 'y-':
                for j in range(nbre_points):
                    x = np.append(x, x[-1] * nbre_points)
                    y = np.append(y, y[-1] - increment)

            elif direction == 'x+':
                for j in range(nbre_points):
                    y = np.append(y, y[-1])
                    x = np.append(x, x[-1] + increment)

            elif direction == 'x-':
                for j in range(nbre_points):
                    y = np.append(y, y[-1])
                    x = np.append(x, x[-1] - increment)

        # Si le tronçon est un coude
        elif liste_geometrie[i][:-2] == 'coude':
            x_coude, y_coude = calculer_coordonnees_coude(x[-1], y[-1], liste_rayon[i], 90, liste_geometrie[i][-1], direction)

            y = np.append(y, y_coude)
            x = np.append(x, x_coude)

            if liste_geometrie[i][-1] == 'D':
                if direction == 'y+':
                    direction = 'x+'
                elif direction == 'y-':
                    direction = 'x-'
                elif direction == 'x+':
                    direction = 'y-'
                else:
                    direction = 'y+'
            elif liste_geometrie[i][-1] == 'G':
                if direction == 'y+':
                    direction = 'x-'
                elif direction == 'y-':
                    direction = 'x+'
                elif direction == 'x+':
                    direction = 'y+'
                else:
                    direction = 'y-'

    return x,y


def tracer_canalisations(canalisation):
    """Cette procédure permet de tracer la canalisation.

    :param canalisation: La canalisation à tracer
    :type canalisation: Canalisation
    """
    x_guide, y_guide = calculer_coordonnees_guide(canalisation,0,0)
    plt.plot(x_guide,y_guide)
    plt.axis('equal')
    plt.xlabel("Longueur en m")
    plt.ylabel("Longueur en m")
    plt.title("Tracé de la géométrie du problème")
    plt.grid()
    plt.show()


def tracer_pression_vitesse_1d(liste_pression, liste_vitesse, liste_abscisse, liste_longueur):
    """Cette procédure permet de tracer les variations de pression et de vitesse le long de la canalisation.

    :param liste_pression: La variation de pression dans la canalisation
    :type liste_pression: list
    :param liste_vitesse: La variation de vitesse dans la canalisation
    :type liste_vitesse: list
    :param liste_abscisse: La liste des abscisses de la canalisation
    :type liste_abscisse: list
    :param liste_longueur: La liste des longueurs de chaque géométrie de la canalisation
    :type liste_longueur: list
    """
    print("...Tracé de la pression...")
    plt.plot(liste_abscisse, liste_pression, label='Pression')
    liste_longueur = liste_longueur[:-1]
    abscisse_geo = 0

    # Tracé des changements de géométrie
    for idx in range(len(liste_longueur)):
        abscisse_geo += liste_longueur[idx]
        plt.axvline(abscisse_geo, color='r', linestyle='--', label=f'Changement de géométrie {idx + 1}')

    plt.title("Évolution de la pression le long de la canalisation, en longueur linéaire")
    plt.xlabel("Longueur linéaire en m")
    plt.ylabel("Pression en Pa")
    plt.legend()
    plt.show()

    # print("...Tracé de la vitesse...")
    # plt.plot(liste_abscisse, liste_vitesse, label='Vitesse')
    # abscisse_geo = liste_longueur[0]
    # for idx in range(len(liste_longueur)):
    #     plt.axvline(abscisse_geo, color='r', linestyle='--', label=f'Changement de géométrie {idx + 1}')
    #     abscisse_geo += liste_longueur[idx]
    # plt.title("Évolution de la pression le long de la canalisation, en longueur linéaire")
    # plt.xlabel("Longueur linéaire en m")
    # plt.ylabel("Vitesse en m/s")
    # plt.legend()
    # plt.show()
