"""
File : calculs.py
Author : Alexis Markiewicz
Date : 2024-07-08
Description : Ce script permet de définir des fonctions qui permettent de calculer les pertes de charges et coefficients associés
"""

# Imports
import numpy as np

# Définition des constantes
g = 9.81


# Définition des fonctions
def calculer_reynolds(vitesse, diametre, viscosite_cine):
    """
    Cette fonction calcule le nombre de Reynolds.

    Args :
        vitesse (float) : La vitesse du fluide, en m/s
        diametre (float) : Le diamètre de la canalisation, en m
        viscosite_cine (float) : La viscosité cinématique de fluide, en m**2/s

    Returns :
        flaot : Le nombre de Reynolds calculé à partir de ces paramètres
    """
    re = vitesse * diametre / viscosite_cine
    return re


def calculer_debit2vitesse(debit, diametre, section):
    """
        Cette fonction convertit un débit en vitesse.

        Args :
            debit (float) : Le débit du fluide, en m**3/s
            diametre (float) : Le diamètre de la canalisation, en m
            section (str) : La forme de la section (par exemple 'rond')

        Returns :
            flaot : La vitesse correspondant à ces paramètres
        """
    surface = 1
    # Si la section est ronde
    if section == 'rond':
        surface = np.pi*(diametre/2)**2
    elif section == 'carre':
        surface = diametre**2
    return debit/surface


def calculer_coef_perte_de_charge(reynolds, rugosite, diametre):
    """
        Cette fonction calcule le coefficient de perte de charge régulière, selon le nombre de Reynolds.

        Args :
            reynolds (float) : Le nombre de Reynolds, sans dimension
            rugosite (float) : La rugosité de la canalisation, en m
            diametre (float) : Le diamètre de la canalisation, en m

        Returns:
            flaot : Le coefficient de perte de charge
        """
    # formules trouvées sur : https://fr.wikipedia.org/wiki/%C3%89quation_de_Darcy-Weisbach
    if reynolds < 2320:
        # Loi de Hagen-Poiseuille
        return 64 / reynolds
    else:
        if rugosite == 0:
            # Correlation de Blasius
            return 0.3164 * reynolds ** (-1/4)

        # Corrélation de Serguides
        a = -2 * np.log10((rugosite/(diametre*3.7) + 12/reynolds))
        b = -2 * np.log10((rugosite/(diametre*3.7) + 2.51*a/reynolds))
        c = -2 * np.log10((rugosite/(diametre*3.7) + 2.51*b/reynolds))
        return a - ((b-a)**2)/(c-2*b+a)


def calculer_perte_reguliere(longueur, diametre, vitesse, viscosite_cine, rugosite, densite):
    """
        Cette fonction calcule la différence de pression due aux pertes de charges régulières.

        Args:
            longueur (float) : La longueur de la canalisation, en m
            diametre (float) : Le diamètre de la canalisation, en m
            vitesse (float) : La vitesse du fluide, en m/s
            viscosite_cine (float) : La viscosité cinématique de fluide, en m**2/s
            rugosite (float) : La rugosité de la canalisation, en m
            densite (float) : La densité du fluide en kg/m**3

        Returns:
            flaot : La différence de pression causée par les pertes de charge régulières
    """
    reynolds = calculer_reynolds(vitesse, diametre, viscosite_cine)
    fd = calculer_coef_perte_de_charge(reynolds, rugosite, diametre)
    # formule trouvée sur : https://fr.wikipedia.org/wiki/%C3%89quation_de_Darcy-Weisbach
    return fd * longueur * densite * vitesse**2 / (diametre * 2)


def calculer_perte_chgt_brusque_section(vitesse, diametre_entree, densite, diametre_sortie):
    """
        Cette fonction calcule la différence de pression due aux pertes de charges singulières causées par un
        changement de section brusque.

        Args:
            vitesse (float) : La vitesse du fluide, en m/s
            diametre_entree (float) : Le diamètre à la sortie de la canalisation précédente, en m
            diametre_sortie (float) : Le diamètre à l'entrée de la canalisation courante, en m
            densite (float) : La densité du fluide en kg/m**3

        Returns:
            flaot : La différence de pression causée par les pertes de charge régulières
    """
    # On utilise les formules trouvées sur : https://gpip.cnam.fr/ressources-pedagogiques-ouvertes/hydraulique/co/3grain_PertesChargeVariationsSectionConduite.html
    if diametre_entree < diametre_sortie:
        ksi = (1 - diametre_entree/diametre_sortie)**2
    else:
        C = 0.63 + 0.37 * (diametre_sortie/diametre_entree)**2
        ksi = (1/C - 1)**2
    return densite * ksi * vitesse ** 2 / 2


def calculer_pression_sortie_pompe(puissance, rendement, debit, pression_entree):
    """
        Cette fonction calcule la pression en sortie d'une pompe.

        Args:
            puissance (float) : La puissance de la pompe, en W
            rendement (float) : Le rendement de la pompe, entre 0 et 1
            debit (float) : Le débit de fluide, en m**3/s
            pression_entree (float) : La pression à l'entrée de la pompe, en Pa

        Returns:
            flaot : La valeur de la pression du fluide en sortie de pompe
    """
    return pression_entree + rendement * puissance/debit


def calculer_perte_singuliere(coef_perte_signuliere, densite, vitesse):
    """
        Cette fonction calcule la différence de pression due aux pertes de charges singulières.

        Args:
            coef_perte_signuliere (float) : Le coefficient de perte de charge singulière
            densite (float) : La densité du fluide en kg/m**3
            vitesse (float) : La vitesse du fluide, en m/s

        Returns:
            flaot : La différence de pression causée par les pertes de charge singulières
    """
    # formule trouvée sur : https://fr.wikipedia.org/wiki/Perte_de_charge
    return coef_perte_signuliere * densite * vitesse**2 / 2
