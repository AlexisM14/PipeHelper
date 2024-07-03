"""Ce script définit toutes les classes qui seront utiles au programme"""
import numpy as np

from calculs import *
from gestion_BDD_geometries import *
import matplotlib.pyplot as plt


class Troncon:

    # Méthode constructeur
    def __init__(self, longueur, section, diametre, materiau, rugosite, geometrie, courbure, fluide, vitesse_init, pression_init, temperature_init, densite, viscosite_cine):
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
        if viscosite_cine == 0:
            self.viscosite_cine = recuperer_valeur_fluide(fluide, temperature_init, 'Viscosité cinématique')
        else:
            self.viscosite_cine = viscosite_cine
        if densite == 0:
            self.densite = recuperer_valeur_fluide(fluide, temperature_init, 'Masse volumique')
        else:
            self.densite = densite

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

    def ajouter_vitesse(self, vitesse):
        self.vitesse_init = vitesse

    def ajouter_pression(self, pression):
        self.pression_init = pression

    def ajouter_temperature(self, temperature):
        self.temperature_init = temperature

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

    def renvoyer_liste_pression(self):
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_pression())
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

    def calculer_distrib_pression_vitesse(self):
        liste_geometrie = self.renvoyer_liste_geometrie()
        liste_longueur = self.renvoyer_liste_longueur()
        troncon = self.renvoyer_troncon(0)
        nbre_troncon = self.recupere_nbre_troncons()

        densite = troncon.recuperer_densite()

        liste_pression = [troncon.recuperer_pression()]
        liste_vitesse = [troncon.recuperer_vitesse()]
        liste_temperature = [troncon.recuperer_temperature()]
        liste_abscisse = [0]

        for i in range(0,nbre_troncon):
            troncon = self.renvoyer_troncon(i)
            pression_entree = liste_pression[-1]
            vitesse_entree = liste_vitesse[-1]
            temperature_entree = liste_temperature[-1]
            longueur = liste_longueur[i]
            diametre = troncon.recuperer_diametre()

            # Calcul des pertes de charges et pression de sortie
            delta_reguliere = calculer_perte_reguliere(longueur, diametre, vitesse_entree, troncon.recuperer_viscosite_cine(), troncon.recuperer_rugosite(), densite)
            coef_singuliere = recuperer_coeff_perte_charge_singuliere(liste_geometrie[i][:-2], 90, diametre, diametre, troncon.recuperer_courbure())
            delta_singuliere = calculer_perte_singuliere(coef_singuliere, densite, vitesse_entree)
            delta_pression = delta_singuliere + delta_reguliere
            print(f"Sortie tronçon {i}")
            print(f"Regu : {delta_reguliere}")
            print(f"Singu : {delta_singuliere}")
            print("")
            pression_sortie = pression_entree - delta_pression

            vitesse_sortie = calculer_vitesse_sortie(vitesse_entree, pression_entree, pression_sortie, delta_reguliere, densite, coef_singuliere)
            temperature_sortie = calculer_temperature_sortie(temperature_entree)

            liste_pression = np.append(liste_pression, pression_sortie)
            liste_vitesse = np.append(liste_vitesse, vitesse_sortie)
            liste_temperature = np.append(liste_temperature, temperature_sortie)
            liste_abscisse = np.append(liste_abscisse, liste_abscisse[-1] + liste_longueur[i])
            troncon.ajouter_pression(pression_sortie)
            troncon.ajouter_vitesse(vitesse_sortie)
            troncon.ajouter_temperature(temperature_sortie)

        liste_abscisse_discrete = []
        liste_pression_discrete =[]
        liste_vitesse_discrete = []
        liste_temperature_discrete =[]

        for i in range(nbre_troncon):
                longueur = liste_longueur[i]
                nbre_points = int(longueur*100)

                liste_pression_discrete = np.append(liste_pression_discrete, np.linspace(liste_pression[i], liste_pression[i+1], nbre_points)[:-1])
                liste_vitesse_discrete = np.append(liste_vitesse_discrete, np.linspace(liste_vitesse[i], liste_vitesse[i+1], nbre_points)[:-1])
                liste_temperature_discrete = np.append(liste_temperature_discrete, np.linspace(liste_abscisse[i], liste_abscisse[i+1], nbre_points)[:-1])
                liste_abscisse_discrete = np.append(liste_abscisse_discrete, np.linspace(liste_abscisse[i], liste_abscisse[i + 1], nbre_points)[:-1])

        return liste_pression_discrete, liste_vitesse_discrete, liste_temperature_discrete, liste_abscisse_discrete, liste_longueur

    def tracer_pression_vitesse_1d(self):
        liste_pression, liste_vitesse, liste_temperature, liste_abscisse, liste_longueur = self.calculer_distrib_pression_vitesse()

        print("...Tracé de la pression...")
        plt.plot(liste_abscisse, liste_pression, label='Pression')
        # for i in range(len(liste_longueur)):
        #     plt.axvline(liste_longueur[i], color='r', linestyle='--', label=f"Changement {i+1} de géométrie")
        plt.title("Évolution de la pression le long de la canalisation, en longueur linéaire")
        plt.xlabel("Longueur linéaire en m")
        plt.ylabel("Pression en Pa")
        plt.legend()
        plt.show()

        print("...Tracé de la vitesse...")
        plt.plot(liste_abscisse, liste_vitesse, label='Vitesse')
        # for i in range(len(liste_longueur)):
        #     plt.axvline(liste_longueur[i], color='r', linestyle='--', label=f"Changement {i+1} de géométrie")
        plt.title("Évolution de la pression le long de la canalisation, en longueur linéaire")
        plt.xlabel("Longueur linéaire en m")
        plt.ylabel("Vitesse en m/s")
        plt.legend()
        plt.show()

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
