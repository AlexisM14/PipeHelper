import numpy as np
from verifications import *
from classes import *
from GestionBDDFluide import *
from GestionBDDMateriau import *
from affichage import *

g = 9.81


# Définition de la fonction qui calcule le nombre de reynolds
def calculer_reynolds(vitesse, diametre, viscosite_cine):
    """Calcule le nombre de Reynolds"""
    # vitesse en m/s - diametre en m - viscorsite_cine en m2/s
    return vitesse * diametre / viscosite_cine


# Définition de la fonction qui calcule le coefficient de perte de charge
def calculer_coef_perte_de_charge(reynolds, rugosite, diametre):
    """Renvoie le coefficient de perte de charge selon le nomre de Reynolds"""
    # rugosite et diametre en mm - reynolds sans unite
    # formule https://fr.wikipedia.org/wiki/%C3%89quation_de_Darcy-Weisbach
    if reynolds < 2320:
        # Loi de Hagen-Poiseuille
        return 64 / reynolds
    else:
        if rugosite == 0:
            # Correlation de Blasius
            return 0.3164 * reynolds ** (1/4)

        # Corrélation de Serguides
        A = -2 * np.log10((rugosite/(diametre*3.7) + 12/reynolds))
        B = -2 * np.log10((rugosite/(diametre*3.7) + 2.51*A/reynolds))
        C = -2 * np.log10((rugosite/(diametre*3.7) + 2.51*B/reynolds))
        return A - ((B-A)**2)/(C-2*B+A)


def calculer_coef_perte_charge_coude(rayon_courbure, diametre, angle):
    if angle == 90:
        return
    elif angle == 45:
        return


# Définition de la fonction de calcul de pression selon la formule de Poiseuille
def calculer_pression_poiseuille(debit_vol, viscosite_cine, pression_entree, longueur_canal, rayon_canal):
    """Renvoie la pression de sortie dans un écoulement de Poiseuille"""
    # debit_col en m3/s - viscosite_cine en m2/s - pression_entree en Pa - longueur_canal, rayon_canal en m
    return pression_entree - 8 * viscosite_cine * longueur_canal * debit_vol / (np.pi * rayon_canal**4)


# Définition de la fonction qui calcule les pertes de charges régulières
def calculer_perte_reguliere(longueur, diametre, vitesse, viscosite_cine, rugosite, densite, pression_entree):
    """Renvoie la pression en sortie d'un endroit pouvant provoquer une perte de charge régulière"""
    # longueur, diametre, rugosite en m - vitesse en m/s - viscosite_cine en m2/s - densite en kg/m2 -
    # pression_entree en Pa
    reynolds = calculer_reynolds(vitesse, diametre, viscosite_cine)
    fd = calculer_coef_perte_de_charge(reynolds, rugosite, diametre)
    return pression_entree - fd * longueur * densite * vitesse**2 / diametre * 2


# Définition de la fonction qui calcule les pertes de charges liée à un changement brusque de section
def calculer_perte_chgt_brusque_section(vitesse, section_entree, densite, section_sortie, pression_entree):
    """Renvoie la pression en sortie d'un changement brusaue de section"""
    # vitesse en m/s - section_entree, section_sortie en m - densite en kg/m3 - pression_entree en Pa
    if section_entree < section_sortie:
        ksi = (1 - section_entree/section_sortie)**2
        # il faut multiplier par la vitesse d'entrée
        return pression_entree + densite * ksi * vitesse ** 2 / 2
    else:
        C = 0.63 + 0.37 * (section_sortie/section_entree)**2
        ksi = (1/C - 1)**2
        # il faut multiplier par la vitesse de sortie
        return pression_entree - densite * ksi * vitesse ** 2 / 2


# Définition de la fonction qui renvoie la pression en sortie de la pompe
def calculer_pression_sortie_pompe(puissance, rendement, debit, pression_entree):
    """Renvoie la pression en sortie d'une pompe"""
    # puissance en W - debit en m3/s - pression_entree en Pa - rendement sans unité
    return pression_entree + rendement * puissance/debit


def calculer_vitesse_troncon():
    return True


def calculer_vitesse():
    return True


def calculer_temperature_troncon():
    return True


def calculer_temperature():
    return True

