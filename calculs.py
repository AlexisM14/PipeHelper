
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
    """Cette fonction calcule le nombre de Reynolds.

    :param vitesse: La vitesse du fluide, en m/s
    :type vitesse: float
    :param diametre: Le diamètre de la canalisation, en m
    :type diametre: float
    :param viscosite_cine: La viscosité cinématique de fluide, en m**2/s
    :type viscosite_cine: float

    :return: Le nombre de Reynolds calculé à partir de ces paramètres
    :rtype: float
    """

    re = vitesse * diametre / viscosite_cine
    return re


def calculer_debit2vitesse(debit, diametre, section):
    """Cette fonction calcule le coefficient de perte de charge régulière, selon le nombre de Reynolds.

    :param debit: Le débit du fluide, en m**3/s
    :type debit: float
    :param diametre: Le diamètre de la canalisation, en m
    :type diametre: float
    :param section: La forme de la section (par exemple 'rond')
    :type section: str

    :return: La vitesse correspondant à ces paramètres
    :rtype: float
    """

    surface = 1
    # Si la section est ronde
    if section == 'rond':
        surface = np.pi*(diametre/2)**2
    elif section == 'carre':
        surface = diametre**2
    return debit/surface


def calculer_coef_perte_de_charge(reynolds, rugosite, diametre):
    """Cette fonction calcule le coefficient de perte de charge régulière, selon le nombre de Reynolds.

    :param reynolds: Le nombre de Reynolds, sans dimension
    :type reynolds: float
    :param rugosite: La rugosité de la canalisation, en m
    :type rugosite: float
    :param diametre: Le diamètre de la canalisation, en m
    :type diametre: float

    :return: Le coefficient de perte de charge
    :rtype: float
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
    """Cette fonction calcule la différence de pression due aux pertes de charges régulières.

    :param longueur: La longueur de la canalisation, en m
    :type longueur: float
    :param diametre: Le diamètre de la canalisation, en m
    :type diametre: float
    :param vitesse: La vitesse du fluide, en m/s
    :type vitesse: float
    :param viscosite_cine: La viscosité cinématique de fluide, en m**2/s
    :type viscosite_cine: float
    :param rugosite: La rugosité de la canalisation, en m
    :type rugosite: float
    :param densite: La densité du fluide, en kg/m**3
    :type densite: float

    :return: La différence de pression causée par les pertes de charge régulières
    :rtype: float
    """

    reynolds = calculer_reynolds(vitesse, diametre, viscosite_cine)
    fd = calculer_coef_perte_de_charge(reynolds, rugosite, diametre)
    # formule trouvée sur : https://fr.wikipedia.org/wiki/%C3%89quation_de_Darcy-Weisbach
    return fd * longueur * densite * vitesse**2 / (diametre * 2)


def calculer_perte_chgt_brusque_section(vitesse, diametre_entree, densite, diametre_sortie):
    """Cette fonction calcule la différence de pression due aux pertes de charges singulières causées par un
        changement de section brusque.

    :param vitesse: La vitesse du fluide, en m/s
    :type vitesse: float
    :param diametre_entree: Le diamètre de la canalisation, en m
    :type diametre_entree: float
    :param densite: La densité du fluide, en kg/m**3
    :type densite: float
    :param diametre_sortie: Le diamètre de la canalisation, en m
    :type diametre_sortie: float

    :return: La différence de pression causée par les pertes de charge
    :rtype: float
    """

    # On utilise les formules trouvées sur : https://gpip.cnam.fr/ressources-pedagogiques-ouvertes/hydraulique/co/3grain_PertesChargeVariationsSectionConduite.html
    if diametre_entree < diametre_sortie:
        ksi = (1 - diametre_entree/diametre_sortie)**2
    else:
        C = 0.63 + 0.37 * (diametre_sortie/diametre_entree)**2
        ksi = (1/C - 1)**2
    return densite * ksi * vitesse ** 2 / 2


def calculer_pression_sortie_pompe(puissance, rendement, debit, pression_entree):
    """Cette fonction calcule la pression en sortie d'une pompe.

    :param puissance: La puissance de la pompe, en W
    :type puissance: float
    :param rendement: Le rendement de la pompe, entre 0 et 1
    :type rendement: float
    :param debit: Le debit de la canalisation, en m**3/s
    :type debit: float
    :param pression_entree: La pression en entrée de la pompe, en Pa
    :type pression_entree: float

    :return: La valeur de la pression du fluide en sortie de pompe
    :rtype: float
    """

    return pression_entree + rendement * puissance/debit


def calculer_perte_singuliere(coef_perte_signuliere, densite, vitesse):
    """Cette fonction calcule la différence de pression due aux pertes de charges singulières.

    :param coef_perte_signuliere: Le coefficient de perte de charge singuliètre, sans unité
    :type coef_perte_signuliere: float
    :param densite: La densité du fluide, en kg/m**3
    :type densite: float
    :param vitesse: La vitesse du fluide, en m/s
    :type vitesse: float

    :return: La différence de pression causée par les pertes de charge singulières
    :rtype: float
    """

    # formule trouvée sur : https://fr.wikipedia.org/wiki/Perte_de_charge
    return coef_perte_signuliere * densite * vitesse**2 / 2
