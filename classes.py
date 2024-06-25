"""Ce script définit toutes les classes qui seront utiles au programme"""
import numpy as np


class Troncon:

    # Méthode constructeur
    def __init__(self):
        self.liste_attributs = np.zeros(1)
        # Les attributs doivent être enregistrés dans l'ordre : longueur, forme de la section, diamètre, rugosité,
        # forme du tronçon, angle du troçon,
        self.len = 0

    def ajouter_attribut(self, attribut):
        if self.len == 0:
            self.liste_attributs[0] = attribut
        else:
            np.append(self.liste_attributs, attribut)
        self.len += 1

    def supprimer_attribut(self, position):
        np.delete(self.liste_attributs, position)
        self.len -= 1


class Canalisation:

    # Méthode constructeur
    def __init__(self):
        self.liste_troncons = np.zeros(1)
        # Les attributs doivent être enregistrés dans l'ordre : longueur, forme de la section, diamètre, rugosité,
        # forme du tronçon, angle du troçon,
        self.len = 0

    def ajouter_troncon(self, troncon):
        if self.len == 0:
            self.liste_troncons[0] = troncon
        else:
            np.append(self.liste_troncons, attribut)
        self.len += 1

    def renvoyer_longueur(self):
        liste_longueur = np.zeros(self.len)
        for i in range(self.len):
            liste_longueur[i] = self.liste_troncons[i][0]
        return liste_longueur

    def renvoyer_forme_troncon(self):
        liste_formes = np.zeros(self.len)
        for i in range(self.len):
            liste_formes[i] = self.liste_troncons[i][4]
        return liste_formes

    def renvoyer_angle_troncon(self):
        liste_angles = np.zeros(self.len)
        for i in range(self.len):
            liste_angles[i] = self.liste_troncons[i][5]
        return liste_angles
