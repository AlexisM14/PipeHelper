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
    """Classe qui modélise un tronçon

    :param longueur: La longueur du tronçon, en m
    :type longueur: float
    :param section: La forme de la section du tronçon
    :type section: str
    :param diametre: Le diamètre de la section du tronçon, en m
    :type diametre: float
    :param materiau: Le matériau du tronçon
    :type materiau: str
    :param rugosite: La rugosité du tronçon, en m
    :type rugosite: float
    :param geometrie: La géométrie du tronçon ('droit', 'coude D' ou 'coude G')
    :type geometrie: str
    :param courbure: Le rayon de courbure du tronçon, s'il y a lieu, en m
    :type courbure: float
    :param fluide: Le nom du fluide parcourant le tronçon
    :type fluide: str
    :param vitesse_init: La vitesse du fluide dans à l'entrée du tronçon, en m/s
    :type vitesse_init: float
    :param pression_init: La pression du fluide dans à l'entrée du tronçon, en Pa
    :type pression_init: float
    :param temperature_init: La température du fluide à l'entrée du tronçon, en °C
    :type temperature_init: float
    :param densite: La densité du fluide, en kg/m**3
    :type densite: float
    :param viscosite_cine: La viscosité cinématique du fluide, en m**2/s
    :type viscosite_cine: float
    """

    def __init__(self, longueur, section, diametre, materiau, rugosite, geometrie, courbure, fluide, vitesse_init, pression_init, temperature_init, densite, viscosite_cine):
        """Méthode constructeur
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
        """Cette fonction calcule le nombre de Reynolds du tronçon

        :return: Le nombre de Reynolds du fluide dans ce tronçon
        :rtype: float
        """
        return calculer_reynolds(self.vitesse_init, self.diametre, self.viscosite_cine)

    def calculer_delta_pression_reguliere_troncon(self):
        """Cette fonction calcule la différence de pression due aux pertes de charge régulières du tronçon

        :return: La différence de pression, due aux pertes de charges régulière, entre l'entrée et la sortie du tronçon
        :rtype: float
        """
        return calculer_perte_reguliere(self.longueur, self.diametre, self.vitesse_init, self.viscosite_cine, self.rugosite, self.densite, self.pression_init)

    def calculer_coef_singuliere_troncon(self):
        """Cette fonction calcule le coefficient de perte de charge singulière du tronçon

        :return: Le coefficient de perte de charge singulière du tronçon
        :rtype: float
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
        """Cette fonction calcule la différence de pression due aux pertes de charges singulières du tronçon

        :return: La différence de pression, due aux pertes de charges singulières, entre l'entrée et la sortie du tronçon
        :rtype: float
        """
        coef = self.calculer_coef_singuliere_troncon()
        return calculer_perte_singuliere(coef, self.densite, self.vitesse_init)

    def recuperer_longueur(self):
        """Cette fonction récupère la longueur du tronçon

        :return: La longueur du tronçon
        :rtype: float
        """
        return self.longueur

    def recuperer_section(self):
        """Cette fonction récupère la section du tronçon

        :return: La section du tronçon
        :rtype: float
        """
        return self.section

    def recuperer_diametre(self):
        """Cette fonction récupère le diamètre du tronçon

        :return: Le diamètre du tronçon
        :rtype: float
        """
        return self.diametre

    def recuperer_materiau(self):
        """Cette fonction récupère le matériau du tronçon

        :return: Le matériau du tronçon
        :rtype: str
        """
        return self.materiau

    def recuperer_rugosite(self):
        """Cette fonction récupère la rugosité du tronçon

        :return: La rugosité du tronçon
        :rtype: float
        """
        return self.rugosite

    def recuperer_geometrie(self):
        """Cette fonction récupère la géométrie du tronçon

        :return: n
        :rtype: str
        """
        return self.geometrie

    def recuperer_courbure(self):
        """Cette fonction récupère le rayon de courbure du tronçon

        :return: Le rayon de courbure du tronçon
        :rtype: float
        """
        return self.courbure

    def recuperer_fluide(self):
        """Cette fonction récupère le nom du fluide  du tronçon

        :return: Le nom du fluide du tronçon
        :rtype: str
        """
        return self.fluide

    def recuperer_vitesse(self):
        """Cette fonction récupère la vitesse dans le tronçon

        :return: La vitesse dans le tronçon
        :rtype: float
        """
        return self.vitesse_init

    def recuperer_pression(self):
        """ Cette fonction récupère la pression du fluide dans le tronçon

        :return: La pression du fluide dans le tronçon
        :rtype: float
        """
        return self.pression_init

    def recuperer_temperature(self):
        """Cette fonction récupère la température du fluide dans le tronçon

        :return: La température du fluide dans le tronçon
        :rtype: float
        """
        return self.temperature_init

    def recuperer_viscosite_cine(self):
        """Cette fonction récupère la viscosité cinématique du fluide dans le tronçon

        :return: La viscosité cinématique du fluide dans le tronçon
        :rtype: float
        """
        return self.viscosite_cine

    def recuperer_densite(self):
        """Cette fonction récupère la densité du fluide dans le tronçon

        :return: La densité du fluide dans le tronçon
        :rtype: float
        """
        return self.densite

    def ajouter_vitesse(self, vitesse):
        """Cette fonction permet d'ajouter / actualiser une vitesse au fluide du tronçon

        :param vitesse: La vitesse du fluide, en m/s
        :type vitesse: float
        """
        self.vitesse_init = vitesse

    def ajouter_pression(self, pression):
        """Cette fonction permet d'ajouter / actualiser une pression au fluide du tronçon

        :param pression: La pression du fluide, en Pa
        :type pression: float
        """
        self.pression_init = pression

    def ajouter_temperature(self, temperature):
        """
        Cette fonction permet d'ajouter / actualiser une température au fluide du tronçon

        :param temperature: La temperature du fluide, en °C
        :type temperature: float
        """
        self.temperature_init = temperature

    def afficher(self):
        """Cette fonction permet d'afficher les attributs du tronçon
        """

        print(self.longueur, self.section, self.diametre, self.materiau, self.rugosite ,self.geometrie,
              self.courbure, self.fluide, self.vitesse_init, self.pression_init, self.temperature_init,
              self.viscosite_cine, self.densite)


class Canalisation():
    """Classe qui représente une canalisation, soit une liste de tronçons
    """

    def __init__(self):
        """Méthode constructeur
        """

        self.liste_troncons = []
        self.longueur = 0

    def recupere_nbre_troncons(self):
        """Cette fonction récupère le nombre de tronçon dans la canalisation

        :return: Le nombre de tronçon dans la canaliation
        :rtype: int
        """
        return self.longueur

    def renvoyer_troncon(self, idx):
        """Cette fonction renvoie un tronçon de la canalisation

        :param idx: L'index du tronçon à renvoyer
        :type idx: int

        :return: Le tronçon correspondant à idx
        :rtype: Troncon
        """
        if idx < self.longueur:
            return self.liste_troncons[idx]

    def ajouter_troncon(self, troncon):
        """Cette fonction peremt d'ajouter / modifier un tronçon à la canalisation

        :param troncon: Le troncon à ajouter
        :type troncon: Troncon
        """
        self.liste_troncons.append(troncon)
        self.longueur += 1

    def supprimer_troncon(self, idx):
        """Cette fonction permet de supprimer un tronçon de la canalisation

        :param idx: L'index du tronçon à renvoyer
        :type idx: int
        """
        if self.longueur > 1:
            self.longueur -= 1
            self.liste_troncons = np.delete(self.liste_troncons, idx)

    def renvoyer_liste_longueur(self):
        """Cette fonction permet de renvoyer la liste contenant la longueur de chaque tronçon de la canalisation

        :return: La liste des longueurs de chaque tronçon de la canalisation
        :rtype: list
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_longueur())
        return liste

    def renvoyer_liste_section(self):
        """Cette fonction permet de renvoyer la liste contenant la section de chaque tronçon de la canalisation

        :return: La liste des sections de chaque tronçon de la canalisation
        :rtype: list
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_section())
        return liste

    def renvoyer_liste_diametre(self):
        """Cette fonction permet de renvoyer la liste contenant le diamètre de chaque tronçon de la canalisation

        :return: La liste des diamètres de chaque tronçon de la canalisation
        :rtype: list
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_diametre())
        return liste

    def renvoyer_liste_materiau(self):
        """Cette fonction permet de renvoyer la liste contenant le matériau de chaque tronçon de la canalisation

        :return: La liste des matériaux de chaque tronçon de la canalisation
        :rtype: list
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_materiau())
        return liste

    def renvoyer_liste_rugosite(self):
        """Cette fonction permet de renvoyer la liste contenant la rugosité de chaque tronçon de la canalisation

        :return: La liste des rugosités de chaque tronçon de la canalisation
        :rtype: list
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_rugosite())
        return liste

    def renvoyer_liste_geometrie(self):
        """Cette fonction permet de renvoyer la liste contenant la géométrie de chaque tronçon de la canalisation

        :return: La liste des géométries de chaque tronçon de la canalisation
        :rtype: list
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_geometrie())
        return liste

    def renvoyer_liste_pression(self):
        """Cette fonction permet de renvoyer la liste contenant la pression de chaque tronçon de la canalisation

        :return: La liste des pressions de chaque tronçon de la canalisation
        :rtype: list
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_pression())
        return liste

    def renvoyer_liste_courbure(self):
        """Cette fonction permet de renvoyer la liste contenant le rayon de courbure de chaque tronçon de la canalisation

        :return: La liste des rayons de courbure de chaque tronçon de la canalisation
        :rtype: list
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_courbure())
        return liste

    def renvoyer_liste_fluide(self):
        """Cette fonction permet de renvoyer la liste contenant le nom du fluide de chaque tronçon de la canalisation

        :return: La liste des noms de fluide de chaque tronçon de la canalisation
        :rtype: list
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_fluide())
        return liste

    def renvoyer_liste_vitesse(self):
        """Cette fonction permet de renvoyer la liste contenant la vitesse du fluide de chaque tronçon de la canalisation

        :return: La liste des vitesses de fluide de chaque tronçon de la canalisation
        :rtype: list
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_vitesse())
        return liste

    def calculer_distrib_pression_vitesse(self):
        """Cette fonction permet de calculer la distribution de pression, vitesse, température, abscisses et la liste des
        longueur de chaque tronçon de la canalisation

        :return: La liste de la pression le long de la canalisation
        :rtype: list
        :return: La liste de la vitesse le long de la canalisation
        :rtype: list
        :return: La liste de la température le long de la canalisation
        :rtype: list
        :return: La liste de la longueur le long de la canalisation
        :rtype: list
        :return: La liste des longueurs de chaque tronçon
        :rtype: list
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
        """Cette fonction permet de renvoyer la liste contenant la température du fluide de chaque tronçon de la canalisation

        :return: La liste des températures de fluide de chaque tronçon de la canalisation
        :rtype: list
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_temperature())
        return liste

    def renvoyer_liste_viscosite_cine(self):
        """Cette fonction permet de renvoyer la liste contenant la viscosité cinématique du fluide de chaque tronçon de la canalisation

        :return: La liste des viscosité cinématique de fluide de chaque tronçon de la canalisation
        :rtype: list
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_viscosite_cine())
        return liste

    def renvoyer_liste_densite(self):
        """Cette fonction permet de renvoyer la liste contenant la densité du fluide de chaque tronçon de la canalisation

        :return: La liste des densités de fluide de chaque tronçon de la canalisation
        :rtype: list
        """
        liste = []
        for i in self.liste_troncons:
            liste.append(i.recuperer_densite())
        return liste
