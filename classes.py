"""
File: classes.py
Author: Alexis Markiewicz
Date: 2024-07-08
Description: Ce script définit toutes les classes qui seront utiles au programme
"""

# Imports
import numpy as np
import matplotlib.pyplot as plt
from gestion_BDD_fluides import recuperer_valeur_fluide
from calculs import calculer_reynolds, calculer_perte_singuliere, calculer_perte_reguliere
from gestion_BDD_geometries import recuperer_coeff_perte_charge_singuliere


# Définition des classes
class Troncon:

    # Méthode constructeur
    def __init__(self, longueur, section, diametre, materiau, rugosite, geometrie, courbure, fluide, vitesse_init, pression_init, temperature_init, densite, viscosite_cine):
        """
        Méthode constructeur

        Args:
            longueur (float) : La longueur du tronçon, en m
            section (str) : La forme de la section du tronçon
            diametre (float) : Le diamètre de la section du tronçon, en m
            materiau (str) : Le matériau du tronçon
            rugosite (float) : La rugosité du tronçon, en m
            geometrie (str) : La géométrie du tronçon ('droit', 'coude D' ou 'coude G')
            courbure (float) : Le rayon de courbure du tronçon, s'il y a lieu, en m
            fluide (str) : Le nom du fluide parcourant le tronçon
            vitesse_init (float) : La vitesse du fluide dans à l'entrée du tronçon, en m/s
            pression_init (float) : La pression du fluide dans à l'entrée du tronçon , en Pa
            temperature_init (float) : La température du fluide à l'entrée du tronçon, en °C
            densite (flaot) : La densité du fluide, en kg/m**3
            viscosite_cine : La viscosité cinématique du fluide, en m**2/s

        Returns:
            Aucun
        """
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

        # Si la viscosité n'est pas rentrée, on va la chercher dans la BDD
        if viscosite_cine == 0:
            self.viscosite_cine = recuperer_valeur_fluide(fluide, temperature_init, 'Viscosité cinématique')
        else:
            self.viscosite_cine = viscosite_cine

        # Si la densité n'est pas rentrée, on va la chercher dans la BDD
        if densite == 0:
            self.densite = recuperer_valeur_fluide(fluide, temperature_init, 'Masse volumique')
        else:
            self.densite = densite

    def calculer_reynolds_troncon(self):
        """
        Cette fonction calcule le nombre de Reynolds du tronçon

        Args:
            Aucun

        Returns:
            float : Le nombre de Reynolds du fluide dans ce tronçon
        """
        return calculer_reynolds(self.vitesse_init, self.diametre, self.viscosite_cine)

    def calculer_delta_pression_reguliere_troncon(self):
        """
        Cette fonction calcule la différence de pression due aux pertes de charge régulières du tronçon

        Args:
            Aucun

        Returns:
            float : La différence de pression, due aux pertes de charges régulière, entre l'entrée et la sortie du tronçon
        """
        return calculer_perte_reguliere(self.longueur, self.diametre, self.vitesse_init, self.viscosite_cine, self.rugosite, self.densite, self.pression_init)

    def calculer_coef_singuliere_troncon(self):
        """
        Cette fonction calcule le coefficient de perte de charge singulière du tronçon

        Args:
            Aucun

        Returns:
            float : Le coefficient de perte de charge singulière du tronçon
        """
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
        """
        Cette fonction calcule la différence de pression due aux pertes de charges singulières du tronçon

        Args:
            Aucun

        Returns:
            float : La différence de pression, due aux pertes de charges singulières, entre l'entrée et la sortie du tronçon
        """
        coef = self.calculer_coef_singuliere_troncon()
        return calculer_perte_singuliere(coef, self.densite, self.vitesse_init)

    def recuperer_longueur(self):
        """
        Cette fonction récupère la longueur du tronçon

        Args:
            Aucun

        Returns:
            float : La longueur du tronçon
        """
        return self.longueur

    def recuperer_section(self):
        """
        Cette fonction récupère la section du tronçon

        Args:
            Aucun

        Returns:
            str : La section du tronçon
        """
        return self.section

    def recuperer_diametre(self):
        """
        Cette fonction récupère le diamètre du tronçon

        Args:
            Aucun

        Returns:
            float : Le diamètre du tronçon
        """
        return self.diametre

    def recuperer_materiau(self):
        """
        Cette fonction récupère le matériau du tronçon

        Args:
            Aucun

        Returns:
            str : Le matériau du tronçon
        """
        return self.materiau

    def recuperer_rugosite(self):
        """
        Cette fonction récupère la rugosité du tronçon

        Args:
            Aucun

        Returns:
            float : La rugosité du tronçon
        """
        return self.rugosite

    def recuperer_geometrie(self):
        """
        Cette fonction récupère la géométrie du tronçon

        Args:
            Aucun

        Returns:
            str : La géométrie du tronçon
        """
        return self.geometrie

    def recuperer_courbure(self):
        """
        Cette fonction récupère le rayon de courbure du tronçon

        Args:
            Aucun

        Returns:
            float : Le rayon de courbure du tronçon
        """
        return self.courbure

    def recuperer_fluide(self):
        """
        Cette fonction récupère le nom du fluide  du tronçon

        Args:
            Aucun

        Returns:
            str : Le nom du fluide du tronçon
        """
        return self.fluide

    def recuperer_vitesse(self):
        """
        Cette fonction récupère la vitesse dans le tronçon

        Args:
            Aucun

        Returns:
            float : La vitesse dans le tronçon
        """
        return self.vitesse_init

    def recuperer_pression(self):
        """
        Cette fonction récupère la pression du fluide dans le tronçon

        Args:
            Aucun

        Returns:
            float : La pression du fluide dans le tronçon
        """
        return self.pression_init

    def recuperer_temperature(self):
        """
        Cette fonction récupère la température du fluide dans le tronçon

        Args:
            Aucun

        Returns:
            float : La température du fluide dans le tronçon
        """
        return self.temperature_init

    def recuperer_viscosite_cine(self):
        """
        Cette fonction récupère la viscosité cinématique du fluide dans le tronçon

        Args:
            Aucun

        Returns:
            float : La viscosité cinématique du fluide dans le tronçon
        """
        return self.viscosite_cine

    def recuperer_densite(self):
        """
        Cette fonction récupère la densité du fluide dans le tronçon

        Args:
            Aucun

        Returns:
            float : La densité du fluide dans le tronçon
        """
        return self.densite

    def ajouter_vitesse(self, vitesse):
        """
        Cette fonction permet d'ajouter / actualiser une vitesse au fluide du tronçon

        Args:
            vitesse (float) : La vitesse du fluide, en m/s

        Returns:
            Aucun
        """
        self.vitesse_init = vitesse

    def ajouter_pression(self, pression):
        """
        Cette fonction permet d'ajouter / actualiser une pression au fluide du tronçon

        Args:
            pression (float) : La pression du fluide, en Pa

        Returns:
            Aucun
        """
        self.pression_init = pression

    def ajouter_temperature(self, temperature):
        """
        Cette fonction permet d'ajouter / actualiser une température au fluide du tronçon

        Args:
            temperature (float) : La temperature du fluide, en °C

        Returns:
            Aucun
        """
        self.temperature_init = temperature

    def afficher(self):
        """
        Cette fonction permet d'afficher les attributs du tronçon
        Args:
            Aucun

        Returns:
            Aucun
        """

        print(self.longueur, self.section, self.diametre, self.materiau, self.rugosite ,self.geometrie,
              self.courbure, self.fluide, self.vitesse_init, self.pression_init, self.temperature_init,
              self.viscosite_cine, self.densite)


class Canalisation():

    def __init__(self):
        """
        Méthode constructeur

        Args:
            Aucun

        Returns:
            Aucun
        """

        self.liste_troncons = []
        self.longueur = 0

    def recupere_nbre_troncons(self):
        """
        Cette fonction récupère le nombre de tronçon dans la canalisation

        Args:
            Aucun

        Returns:
            int : Le nombre de tronçon dans la canaliation
        """
        return self.longueur

    def renvoyer_troncon(self, idx):
        """
        Cette fonction renvoie un tronçon de la canalisation

        Args:
            idx (int) : L'index du tronçon à renvoyer

        Returns:
            Troncon : Le tronçon correspondant à idx
        """
        if idx < self.longueur:
            return self.liste_troncons[idx]

    def ajouter_troncon(self, troncon):
        """
        Cette fonction peremt d'ajouter / modifier un tronçon à la canalisation

        Args:
            troncon : Le troncon à ajouter

        Returns:
            Aucun
        """
        self.liste_troncons.append(troncon)
        self.longueur += 1

    def supprimer_troncon(self, idx):
        """
        Cette fonction permet de supprimer un tronçon de la canalisation

        Args:
            idx (int) : L'index du tronçon à renvoyer

        Returns:
            Aucun
        """
        if self.longueur > 1:
            self.longueur -= 1
            self.liste_troncons = np.delete(self.liste_troncons, idx)

    def renvoyer_liste_longueur(self):
        """
        Cette fonction permet de renvoyer la liste contenant la longueur de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste des longueurs de chaque tronçon de la canalisation
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_longueur())
        return liste

    def renvoyer_liste_section(self):
        """
        Cette fonction permet de renvoyer la liste contenant la section de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste des sections de chaque tronçon de la canalisation
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_section())
        return liste

    def renvoyer_liste_diametre(self):
        """
        Cette fonction permet de renvoyer la liste contenant le diamètre de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste des diamètres de chaque tronçon de la canalisation
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_diametre())
        return liste

    def renvoyer_liste_materiau(self):
        """
        Cette fonction permet de renvoyer la liste contenant le matériau de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste des matériaux de chaque tronçon de la canalisation
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_materiau())
        return liste

    def renvoyer_liste_rugosite(self):
        """
        Cette fonction permet de renvoyer la liste contenant la rugosité de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste des rugosités de chaque tronçon de la canalisation
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_rugosite())
        return liste

    def renvoyer_liste_geometrie(self):
        """
        Cette fonction permet de renvoyer la liste contenant la géométrie de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste des géométries de chaque tronçon de la canalisation
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_geometrie())
        return liste

    def renvoyer_liste_pression(self):
        """
        Cette fonction permet de renvoyer la liste contenant la pression de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste des pressions de chaque tronçon de la canalisation
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_pression())
        return liste

    def renvoyer_liste_courbure(self):
        """
        Cette fonction permet de renvoyer la liste contenant le rayon de courbure de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste des rayons de courbure de chaque tronçon de la canalisation
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_courbure())
        return liste

    def renvoyer_liste_fluide(self):
        """
        Cette fonction permet de renvoyer la liste contenant le nom du fluide de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste des noms de fluide de chaque tronçon de la canalisation
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_fluide())
        return liste

    def renvoyer_liste_vitesse(self):
        """
        Cette fonction permet de renvoyer la liste contenant la vitesse du fluide de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste des vitesses de fluide de chaque tronçon de la canalisation
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_vitesse())
        return liste

    def calculer_distrib_pression_vitesse(self):
        """
        Cette fonction permet de calculer la distribution de pression, vitesse, température, abscisses et la liste des
        longueur de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste de la pression le long de la canalisation
            list : La liste de la vitesse le long de la canalisation
            list : La liste de la température le long de la canalisation
            list : La liste de la longueur le long de la canalisation
            list : La liste des longueurs de chaque tronçon
        """
        # On récupère toute les listes qui nous intéressent et le nombre de tronçons
        liste_geometrie = self.renvoyer_liste_geometrie()
        liste_longueur = self.renvoyer_liste_longueur()
        troncon = self.renvoyer_troncon(0)
        nbre_troncon = self.recupere_nbre_troncons()

        densite = troncon.recuperer_densite()

        # On initialise les listes de pressionm, vitesse, température, abscisse
        liste_pression = [troncon.recuperer_pression()]
        liste_vitesse = [troncon.recuperer_vitesse()]
        liste_temperature = [troncon.recuperer_temperature()]
        liste_abscisse = [0]

        # Pour chaque troncon
        for i in range(0,nbre_troncon):
            troncon = self.renvoyer_troncon(i)

            # On enregitre les paramètres à l,entrée
            pression_entree = liste_pression[-1]
            vitesse_entree = liste_vitesse[-1]
            temperature_entree = liste_temperature[-1]
            longueur = liste_longueur[i]
            diametre = troncon.recuperer_diametre()

            # On calcule les pertes de charges et la pression, vitesse et température de sortie
            delta_reguliere = calculer_perte_reguliere(longueur, diametre, vitesse_entree, troncon.recuperer_viscosite_cine(), troncon.recuperer_rugosite(), densite)
            coef_singuliere = recuperer_coeff_perte_charge_singuliere(liste_geometrie[i][:-2], 90, diametre, troncon.recuperer_courbure())
            delta_singuliere = calculer_perte_singuliere(coef_singuliere, densite, vitesse_entree)
            delta_pression = delta_singuliere + delta_reguliere

            pression_sortie = pression_entree - delta_pression
            vitesse_sortie = vitesse_entree
            temperature_sortie = temperature_entree

            # On enregistre les données dans les listes
            liste_pression = np.append(liste_pression, pression_sortie)
            liste_vitesse = np.append(liste_vitesse, vitesse_sortie)
            liste_temperature = np.append(liste_temperature, temperature_sortie)
            liste_abscisse = np.append(liste_abscisse, liste_abscisse[-1] + liste_longueur[i])

            # On enregistre les données dans le tronçon
            troncon.ajouter_pression(pression_sortie)
            troncon.ajouter_vitesse(vitesse_sortie)
            troncon.ajouter_temperature(temperature_sortie)

        # On initialise les liste discrétisées
        liste_abscisse_discrete = []
        liste_pression_discrete =[]
        liste_vitesse_discrete = []
        liste_temperature_discrete = []

        # On remplit les listes discrétisées
        for i in range(nbre_troncon):
                longueur = liste_longueur[i]
                nbre_points = int(longueur*100)

                liste_pression_discrete = np.append(liste_pression_discrete, np.linspace(liste_pression[i], liste_pression[i+1], nbre_points)[:-1])
                liste_vitesse_discrete = np.append(liste_vitesse_discrete, np.linspace(liste_vitesse[i], liste_vitesse[i+1], nbre_points)[:-1])
                liste_temperature_discrete = np.append(liste_temperature_discrete, np.linspace(liste_abscisse[i], liste_abscisse[i+1], nbre_points)[:-1])
                liste_abscisse_discrete = np.append(liste_abscisse_discrete, np.linspace(liste_abscisse[i], liste_abscisse[i + 1], nbre_points)[:-1])

        return liste_pression_discrete, liste_vitesse_discrete, liste_temperature_discrete, liste_abscisse_discrete, liste_longueur

    def renvoyer_liste_temperature(self):
        """
        Cette fonction permet de renvoyer la liste contenant la température du fluide de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste des températures de fluide de chaque tronçon de la canalisation
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_temperature())
        return liste

    def renvoyer_liste_viscosite_cine(self):
        """
        Cette fonction permet de renvoyer la liste contenant la viscosité cinématique du fluide de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste des viscosité cinématique de fluide de chaque tronçon de la canalisation
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_viscosite_cine())
        return liste

    def renvoyer_liste_densite(self):
        """
        Cette fonction permet de renvoyer la liste contenant la densité du fluide de chaque tronçon de la canalisation

        Args:
            Aucun

        Returns:
            list : La liste des densités de fluide de chaque tronçon de la canalisation
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_densite())
        return liste
