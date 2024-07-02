"""Ce script définit toutes les classes qui seront utiles au programme"""
from calculs import *
from gestion_BDD_geometries import *


class Troncon:

    # Méthode constructeur
    def __init__(self, longueur, section, diametre, materiau, rugosite, geometrie, courbure, fluide, vitesse_init, pression_init, temperature_init):
        self.longueur = longueur
        self.section = section
        self.diametre = diametre
        self.materiau = materiau
        self.rugosite = rugosite
        self.geometrie = geometrie
        self.courbure = courbure
        self.fluide = fluide
        self.vitesse_init = vitesse_init
        self.pression_init = pression_init
        self.temperature_init = temperature_init
        self.viscosite_cine = recuperer_valeur_fluide(fluide, temperature_init, 'Viscosité cinématique')
        self.densite = recuperer_valeur_fluide(fluide, temperature_init, 'Masse volumique')

    def calculer_reynolds_troncon(self):
        return calculer_reynolds(self.vitesse_init, self.diametre, self.viscosite_cine)

    def calculer_delta_pression_reguliere_troncon(self):
        return calculer_perte_reguliere(self.longueur, self.diametre, self.vitesse_init, self.viscosite_cine, self.rugosite, self.densite, self.pression_init)

    def calculer_coef_singuliere_troncon(self):
        if self.geometrie[:-2] == 'coude':
            geometrie = 'coude'

        elif self.geometrie[:-2] == 'coude droit':
            geometrie = 'coude droit'

        elif self.geometrie[:-2] == 'deviation':
            geometrie = 'deviation'

        else:
            geometrie = self.geometrie
        return recuperer_coeff_perte_charge_singuliere(geometrie, 90, self.diametre, self.diametre, self.courbure)

    def calculer_delta_pression_singuliere_troncon(self):
        coef = self.calculer_coef_singuliere_troncon()
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

    def afficher(self):
        print(self.longueur, self.section, self.diametre, self.materiau, self.rugosite ,self.geometrie,
              self.courbure, self.fluide, self.vitesse_init, self.pression_init, self.temperature_init,
              self.viscosite_cine, self.densite)

class Canalisation(Troncon):

    # Méthode constructeur
    def __init__(self):
        self.liste_troncons = []
        self.longueur = 0

    def recupere_nbre_troncons(self):
        return self.longueur

    def renvoyer_troncon(self, idx):
        if idx < self.longueur:
            return self.liste_troncons[idx]
        return "idx trop grand"

    def ajouter_troncon(self, troncon):
        self.liste_troncons.append(troncon)
        self.longueur += 1

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


# Classe générée par ChatGPT à partir de la requête :
# "Crée une classe de liste dont les index sont circulaire en langage python"
class ListeCirculaire():

    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        return self.data[index % len(self.data)]

    def __setitem__(self, index, value):
        self.data[index % len(self.data)] = value

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)

