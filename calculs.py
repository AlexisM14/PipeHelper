import numpy as np
from verifications import *
from classes import *
from GestionBDDFluide import *
from GestionBDDMateriau import *
from affichage import *

g = 9.81


# Re < 2000 : laminaire
# Re >= 2000 : turbulent
def calculer_reynolds(vitesse, diametre, viscosite_cine):
    """Calcule le nombre de Reynolds"""
    # vitesse en m/s
    # diametre en mm
    # viscorsite_cine en cSt
    return vitesse * diametre / viscosite_cine


# formule https://fr.wikipedia.org/wiki/%C3%89quation_de_Darcy-Weisbach
def calculer_coef_perte_de_charge(reynolds, rugosite, diametre):
    """Renvoie le coefficient de perte de charge selon le nomre de Reynolds"""
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


def calculer_pression_poiseuille(debit_vol, viscosite, pression_entree, longueur_canal, rayon_canal):
    """Renvoie la pression de sortie dans un écoulement de Poiseuille"""
    return pression_entree - 8 * viscosite * longueur_canal * debit_vol / (np.pi * rayon_canal**4)


def calculer_perte_reguliere(longueur, diametre, vitesse, viscosite_cine, rugosite, densite):
    """Renvoie la pression en sortie d'un endroit pouvant provoquer une perte de charge régulière"""
    Re = calculer_reynolds(vitesse, diametre, viscosite_cine)
    fd = calculer_coef_perte_de_charge(Re, rugosite, diametre)
    return fd * longueur * densite * vitesse**2 / diametre * 2


def calculer_perte_chgt_section(vitesse, section_entree, section_sortie, pression_entree):
    """Renvoie la pression en sortie d'un changement brusaue de section"""
    return pression_entree - vitesse**2 * (1 - section_entree/section_sortie)**2 / 2

def calculer_perte_singuliere(coef_perte_singuliere, densite, vitesse, pression_entree):
    """Renvoie la pression en sortie d'un endroit pouvant provoquer une perte de charge singulière"""
    return pression_entree - coef_perte_singuliere * densite * vitesse**2 / 2


def calculer_pression_sortie_pompe(puissance, debit, puissance_entree):
    """Renvoie la pression en sortie d'une pompe"""
    return puissance_entree + puissance/debit


def calculer_vitesse_troncon():
    return True


def calculer_vitesse():
    return True


def calculer_temperature_troncon():
    return True


def calculer_temperature():
    return True

