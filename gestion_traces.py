import numpy as np
import matplotlib.pyplot as plt
from classes import Troncon, Canalisation

# La direction x va de gauche à droite
# La direction y va de haut en bas


def calculer_coordonnees_coude(x_debut, y_debut, rayon, angle_deg, orientation, direction):
    angle_rad = np.radians(angle_deg)

    longueur = np.pi * rayon / 2

    nbre_points = int(longueur * 100)

    angles = np.linspace(0, angle_rad, nbre_points)

    x = np.zeros(nbre_points)
    y = np.zeros(nbre_points)

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


def calculer_coordonnees_guide_v2(canalisation, x_debut, y_debut, direction='y+'):

    liste_longueur = canalisation.renvoyer_liste_longueur()
    liste_geometrie = canalisation.renvoyer_liste_geometrie()
    nbre_troncons = canalisation.recupere_nbre_troncons()
    liste_rayon = canalisation.renvoyer_liste_courbure()
    liste_nbre_pts = []

    x = np.array([x_debut])
    y = np.array([y_debut])

    for i in range(nbre_troncons):
        nbre_points = int(liste_longueur[i] * 100)

        increment = float(liste_longueur[i]) / nbre_points

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
    x_guide, y_guide = calculer_coordonnees_guide_v2(canalisation,0,0)
    plt.plot(x_guide,y_guide)
    plt.axis('equal')
    plt.xlabel("Longueur en m")
    plt.ylabel("Longueur en m")
    plt.title("Tracé de la géométrie du problème")
    plt.grid()
    plt.show()


def tracer_pression_vitesse_1d(liste_pression, liste_vitesse, liste_abscisse, liste_longueur):

    print("...Tracé de la pression...")
    plt.plot(liste_abscisse, liste_pression, label='Pression')
    liste_longueur = liste_longueur[:-1]
    abscisse_geo = 0
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


# Fonction test pour tracer une canalisation
def tracer_canal():
    troncon1 = Troncon(2, 'rond', .05, 'PVC', .002, 'droit', 0, 'eau', 2, 1.018*10**5, 20, .01, .01)
    troncon2 = Troncon(1, 'rond', .05, 'PVC', .002, 'coude G',1,'eau', 2, 1.018*10**5, 20, .01, .01)
    troncon3 = Troncon(1, 'rond', .05, 'PVC', .002, 'coude D',  1, 'eau', 2, 1.018*10**5, 20, .01, .01)
    troncon4 = Troncon(2, 'rond', .05, 'PVC', .002, 'coude D',  2, 'eau', 2, 1.018*10**5, 20, .01, .01)
    troncon5 = Troncon(2, 'rond', .05, 'PVC', .002, 'droit',  3, 'eau', 2, 1.018*10**5, 20, .01, .01)
    troncon6 = Troncon(1, 'rond', .05, 'PVC', .002, 'coude D',  4, 'eau', 2, 1.018*10**5, 20, .01, .01)

    canal = Canalisation()
    canal.ajouter_troncon(troncon1)
    canal.ajouter_troncon(troncon2)
    canal.ajouter_troncon(troncon3)
    canal.ajouter_troncon(troncon4)
    canal.ajouter_troncon(troncon5)
    canal.ajouter_troncon(troncon6)

    tracer_canalisations(canal)


def tracer_coude():
    x = 0
    y = 0
    r = 2
    angle = 90
    sens = 'x-'
    dir = 'coude G'[-1]
    x,y = calculer_coordonnees_coude(x, y, r, angle, dir, sens)
    print(x[-1],y[-1])
    plt.plot(x,y)
    plt.show()

