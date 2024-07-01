"""Ce script définit toutes les classes qui seront utiles au programme"""
from calculs import *


class Troncon:

    # Méthode constructeur
    def __init__(self, longueur, section, diametre, materiau, rugosite, geometrie, angle, courbure, fluide, vitesse_init, pression_init, temperature_init):
        self.liste_attributs = np.zeros(1)
        # Les attributs doivent être enregistrés dans l'ordre : longueur, forme de la section, diamètre, rugosité,
        # forme du tronçon, angle du troçon,
        self.longueur = longueur
        self.section = section
        self.diametre = diametre
        self.materiau = materiau
        self.rugosite = rugosite
        self.geometrie = geometrie
        self.angle = angle
        self.courbure = courbure
        self.fluide = fluide
        self.vitesse_init = vitesse_init
        self.pression_init = pression_init
        self.temperature_init = temperature_init
        self.viscosite_cine = recuperer_valeur_fluide(fluide, temperature_init, 'Viscosité cinématique')
        self.densite = recuperer_valeur_fluide(fluide, temperature_init, 'Masse volumique')

    def ajouter_attribut(self, attribut):
        if self.len == 0:
            self.liste_attributs[0] = attribut
        else:
            np.append(self.liste_attributs, attribut)
        self.len += 1

    def calculer_reynolds_troncon(self):
        return calculer_reynolds(self.vitesse_init, self.diametre, self.viscosite_cine)

    def calculer_delta_pression_reguliere_troncon(self):
        return calculer_perte_reguliere(self.longueur, self.diametre, self.vitesse_init, self.viscosite_cine, self.rugosite, self.densite, self.pression_init)

    def calculer_delta_pression_singuliere_troncon(self):
        if self.geometrie[:-2] == 'coude':
            geometrie = 'coude'

        elif self.geometrie[:-2] == 'coude droit':
            geometrie = 'coude droit'

        elif self.geometrie[:-2] == 'deviation':
            geometrie = 'deviation'

        else:
            geometrie = self.geometrie

        coef = recuperer_coeff_perte_charge_singuliere(geometrie, self.angle, self.diametre, self.diametre, self.courbure)
        return calculer_perte_singuliere(coef, self.densite, self.vitesse_init)

    def recuperer_longueur(self):
        return self.longueur

    def recuperer_section(self):
        return self.section

    def recuperer_diametre(self):
        return self.diametre

    def recuperer_materiau(self):
        return self.materiau

    def recuperer_rugosite(self):
        return self.rugosite

    def recuperer_geometrie(self):
        return self.geometrie

    def recuperer_angle(self):
        return self.angle

    def recuperer_courbure(self):
        return self.courbure

    def recuperer_fluide(self):
        return self.fluide

    def recuperer_vitesse(self):
        return self.vitesse_init

    def recuperer_pression(self):
        return self.pression_init

    def recuperer_temperature(self):
        return self.temperature_init

    def recuperer_viscosite_cine(self):
        return self.viscosite_cine

    def recuperer_densite(self):
        return self.densite


class Canalisation(Troncon):

    # Méthode constructeur
    def __init__(self):
        self.liste_troncons = []
        self.len = 0

    def ajouter_troncon(self, troncon):
        self.liste_troncons.append(troncon)
        self.len += 1

    def renvoyer_liste_longueur(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_longueur())
        return liste

    def renvoyer_liste_section(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_section())
        return liste

    def renvoyer_liste_diametre(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_diametre())
        return liste

    def renvoyer_liste_materiau(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_materiau())
        return liste

    def renvoyer_liste_rugosite(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_rugosite())
        return liste

    def renvoyer_liste_geometrie(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_geometrie())
        return liste

    def renvoyer_liste_angle(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_angle())
        return liste

    def renvoyer_liste_courbure(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_courbure())
        return liste

    def renvoyer_liste_fluide(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_fluide())
        return liste

    def renvoyer_liste_vitesse(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_vitesse())
        return liste

    def renvoyer_liste_pression(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_pression())
        return liste

    def renvoyer_liste_temperature(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_temperature())
        return liste

    def renvoyer_liste_viscosite_cine(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_viscosite_cine())
        return liste

    def renvoyer_liste_densite(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_densite())
        return liste

