import numpy as np
import matplotlib.pyplot as plt

# La direction x va de gauche à droite
# La direction y va de haut en bas


def calculer_coordonnées_coude(x_depart, y_depart, longueur, angle_deg, direction):
    coordonnees_x = np.zeros(1)
    coordonnees_x = np.append(coordonnees_x, x_depart)

    coordonnees_y = np.zeros(1)
    coordonnees_y = np.append(coordonnees_y, y_depart)

    angle_rad = np.deg2rad(angle_deg)
    nbre_points_angle = int(longueur * 100)

    perimetre = longueur * 2 * np.pi / angle_rad
    rayon = perimetre / (2 * np.pi)

    if direction == 'coude B':
        centre_cercle_x = x_depart + rayon
        centre_cercle_y = y_depart
        liste_angles = np.linspace(-np.pi, -np.pi+angle_rad, nbre_points_angle)

    elif direction == 'coude D':
        centre_cercle_x = x_depart
        centre_cercle_y = y_depart - rayon
        liste_angles = np.linspace(np.pi/2, (np.pi/2)+angle_rad, nbre_points_angle)

    elif direction == 'coude G':
        centre_cercle_x = x_depart - rayon
        centre_cercle_y = y_depart
        liste_angles = np.linspace(0,angle_rad, nbre_points_angle)

    else:
        centre_cercle_x = x_depart
        centre_cercle_y = y_depart + rayon
        liste_angles = np.linspace(-np.pi/2, (-np.pi/2)+angle_rad, nbre_points_angle)

    for i in liste_angles:
        x = centre_cercle_x + rayon * np.cos(i)
        y = centre_cercle_y + rayon * np.sin(i)
        coordonnees_x = np.append(coordonnees_x, x)
        coordonnees_y = np.append(coordonnees_y, y)

    return coordonnees_x, coordonnees_y


def calculer_coordonnees_guide(canalisation):
    # liste_longueur = canalisation.renvoyer_longueur()
    # liste_forme = canalisation.renvoyer_forme_troncon()
    # liste_angle = canalisation.renvoyer_angle_troncon()

    # Version ndarrays
    liste_longueur = np.array([])
    liste_forme = np.array([])
    liste_angle = np.array([])
    for i in range(len(canalisation)):
        liste_longueur = np.append(liste_longueur, float(canalisation[i][0]))
        liste_forme = np.append(liste_forme, canalisation[i][4])
        liste_angle = np.append(liste_angle, float(canalisation[i][5]))

    print(liste_longueur)
    longueur_canalisation = np.sum(liste_longueur)

    x_guide = np.array([])
    x_guide = np.append(x_guide, 0)

    y_guide = np.array([])
    y_guide = np.append(y_guide, 0)

    for idx, i in enumerate(liste_forme):
        x_debut_troncon = x_guide[-1]
        y_debut_troncon = y_guide[-1]

        longueur_troncon = liste_longueur[idx]

        angle_troncon = liste_angle[idx]

        if i == 'droit':
            if idx > 0:
                if liste_forme[idx-1][-1] == 'D':
                    for j in range(len(liste_longueur)):
                        x_guide = np.append(x_guide, x_debut_troncon +  liste_longueur[j])
                        y_guide = np.append(y_guide, y_debut_troncon)

                elif liste_forme[idx-1][-1] == 'G':
                    for j in range(len(liste_longueur)):
                        x_guide = np.append(x_guide, x_debut_troncon -  liste_longueur[j])
                        y_guide = np.append(y_guide, y_debut_troncon)

                elif liste_forme[idx-1][-1] == 'B':
                    for j in range(len(liste_longueur)):
                        x_guide = np.append(x_guide, x_debut_troncon)
                        y_guide = np.append(y_guide, y_debut_troncon - liste_longueur[j])

                elif liste_forme[idx-1][-1] == 'H':
                    for j in range(len(liste_longueur)):
                        x_guide = np.append(x_guide, x_debut_troncon)
                        y_guide = np.append(y_guide, y_debut_troncon +  liste_longueur[j])
            else:
                for j in range(len(liste_longueur)):
                    x_guide = np.append(x_guide, x_debut_troncon)
                    y_guide = np.append(y_guide, y_debut_troncon + liste_longueur[j])

        elif i == 'coude D' or i == 'coude G' or i == 'coude B' or i == 'coude H':
            x, y = calculer_coordonnées_coude(x_debut_troncon, y_debut_troncon, float(liste_longueur[idx]),
                                              float(liste_angle[idx]), i)
            print(x,y)
            for j in range(len(x)):
                x_guide = np.append(x_guide, x[j])
                y_guide = np.append(y_guide, y[j])

        else:
            a = 1

    return x_guide, y_guide


def tracer_canalisations(canalisation):
    x_guide, y_guide = calculer_coordonnees_guide(canalisation)
    print(x_guide, y_guide)
    plt.plot(x_guide,y_guide)
    plt.show()


troncon1 = np.array([10, 'rond', 5, 2, 'droit', 0])
troncon2 = np.array([5, 'rond', 5, 2, 'coude D', 90])
troncon3 = np.array([7, 'rond', 5, 2, 'droit', 90])
canal = np.array([troncon1, troncon2, troncon3])

tracer_canalisations(canal)

