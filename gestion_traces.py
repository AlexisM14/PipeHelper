import numpy as np
import matplotlib.pyplot as plt
from classes import Troncon
from classes import Canalisation

# La direction x va de gauche à droite
# La direction y va de haut en bas


def calculer_coordonnees_coude(x_debut, y_debut, longueur, angle_deg, orientation):
    angle_rad = np.radians(angle_deg)

    nbre_points = int(longueur * 100)

    angles = np.linspace(0, angle_rad, nbre_points)

    x = np.zeros(nbre_points)
    y = np.zeros(nbre_points)

    rayon = longueur / angle_rad

    if orientation == 'coude D':
        for i in range(nbre_points):
            x[i] = x_debut + rayon * (1 - np.cos(angles[i]))
            y[i] = y_debut + rayon * np.sin(angles[i])

    elif orientation == 'coude G':
        for i in range(nbre_points):
            x[i] = x_debut - rayon * (1 - np.cos(angles[i]))
            y[i] = y_debut + rayon * np.sin(angles[i])

    elif orientation == 'coude H':
        for i in range(nbre_points):
            x[i] = x_debut + rayon * np.sin(angles[i])
            y[i] = y_debut + rayon * (1 - np.cos(angles[i]))

    elif orientation == 'coude B':
        for i in range(nbre_points):
            x[i] = x_debut + rayon * np.sin(angles[i])
            y[i] = y_debut - rayon * (1 - np.cos(angles[i]))

    return x, y


def calculer_coordonnees_guide_v2(canalisation, x_debut, y_debut, direction='y+'):

    liste_longueur = canalisation.renvoyer_liste_longueur()
    liste_geometrie = canalisation.renvoyer_liste_geometrie()
    nbre_troncons = canalisation.recupere_nbre_troncons()

    x = np.array([x_debut])
    y = np.array([y_debut])

    liste_directions = ['y+', 'x+', 'y-', 'x-']

    for i in range(nbre_troncons):
        nbre_points = int(liste_longueur[i] * 100)
        increment = liste_longueur[i] / nbre_points

        if liste_geometrie[i] == 'droit':
            if i>0 and liste_geometrie[i-1][:-2] == 'coude':
                if liste_geometrie[i-1][-1] == 'D':
                    direction = 'x+'
                elif liste_geometrie[i-1][-1] == 'G':
                    direction = 'x-'
                elif liste_geometrie[i-1][-1] == 'H':
                    direction = 'y+'
                elif liste_geometrie[i-1][-1] == 'B':
                    direction = 'y-'

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
            x_coude, y_coude = calculer_coordonnees_coude(x[-1], y[-1], liste_longueur[i], 90, liste_geometrie[i])
            for j in range(len(x_coude)):
                y = np.append(y, y_coude[j])
                x = np.append(x, x_coude[j])

    return x,y


def tracer_canalisations(canalisation):
    x_guide, y_guide = calculer_coordonnees_guide_v2(canalisation,0,0)
    # print(x_guide, y_guide)
    plt.plot(x_guide,y_guide)
    plt.axis('equal')
    plt.show()


def tracer_pression_1d(liste_pression, liste_longueur):
    plt.plot(liste_longueur, liste_pression)
    plt.title("Évolution de la pression le long de la canalisation, en longueur linéaire")
    plt.xlabel("Longueur en m")
    plt.ylabel("Pression en Pa")
    plt.show()


def tracer_vitesse_1d(liste_vitesse, liste_longueur):
    plt.plot(liste_longueur, liste_vitesse)
    plt.title("Évolution de la vitesse le long de la canalisation, en longueur linéaire")
    plt.xlabel("Longueur en m")
    plt.ylabel("Vitesse en m/s")
    plt.show()


# Fonction test pour tracer une canalisation
def tracer_canal():
    troncon1 = Troncon(2, 'rond', .05, 'PVC', .002, 'droit', 180, .1, 'Eau', 2, 1.018*10**5, 20)
    troncon2 = Troncon(1, 'rond', .05, 'PVC', .002, 'coude D', 90, .1, 'Eau', 2, 1.018*10**5, 20)
    troncon3 = Troncon(1, 'rond', .05, 'PVC', .002, 'droit', 180, .1, 'Eau', 2, 1.018*10**5, 20)
    troncon4 = Troncon(2, 'rond', .05, 'PVC', .002, 'coude H', 180, .1, 'Eau', 2, 1.018*10**5, 20)
    troncon5 = Troncon(2, 'rond', .05, 'PVC', .002, 'coude G', 180, .1, 'Eau', 2, 1.018*10**5, 20)
    troncon6 = Troncon(1, 'rond', .05, 'PVC', .002, 'droit', 180, .1, 'Eau', 2, 1.018*10**5, 20)

    canal = Canalisation()
    canal.ajouter_troncon(troncon1)
    canal.ajouter_troncon(troncon2)
    canal.ajouter_troncon(troncon3)
    canal.ajouter_troncon(troncon4)
    canal.ajouter_troncon(troncon5)

    tracer_canalisations(canal)


def tracer_coude():
    x = 0
    y = 0
    l = 10
    angle = 90
    dir = 'coude D'
    print(x,y)
    x,y = calculer_coordonnees_coude(x, y, l, angle, dir)
    plt.plot(x,y)
    plt.show()


liste_longueur1 = [0, 2, 3, 7, 10]
liste_pression1 = [1.018, 1.013, 1.004, 0.998, 0.9]
liste_vitesse1 = [5, 4, 4.5, 4.2, 3]

# tracer_pression_1d(liste_pression1, liste_longueur1)
# tracer_vitesse_1d(liste_vitesse1, liste_longueur1)

