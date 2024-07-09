"""
File: gestion_YAML.py
Author: Alexis Markiewicz
Date: 2024-07-08
Description: Ce script permet de définir des fonctions qui permettent de manipuler des fichiers .yaml.
Une partie du code est repris du cours MGA802
"""

# Imports
from LecteurYAML import LecteurYAML
import os


# Définition des fonctions
def get_name_yaml():
    """Cette fonction permet de récupérer le nom du fichier .yaml.

    :return: nom du fichier .yaml
    :rtype: strç
    """
    nom = input("--> ")
    while not os.path.exists(nom):
        print(" Le fichier indiqué n'existe pas, entrez le nom du fichier sous la forme : [mon_fichier.txt]")
        nom = input("--> ")
    return nom


def get_info_yaml(nom):
    """Cette procédure permet de récupérer les informations du fichier .yaml.

    :param nom: Le nom du fichier .yaml
    :type nom: str

    :return: Le nom du fluide
    :rtype: str
    :return: Le nombre de tronçons
    :rtype: int
    :return: Le nom du matériau de la canalisation
    :rtype: str
    :return: La rugosité de la canalisation, en m
    :rtype: float
    :return: La forme de la section de la canalisation
    :rtype: str
    :return: Le diamètre de la canalisation, en m
    :rtype: float
    :return: La vitesse intiale, en m/s
    :rtype: float
    :return: Le débit, m**3/s
    :rtype: float
    :return: à La température initiale, en °C
    :rtype: float
    :return: La pression initiale, en Pa
    :rtype: float
    :return: La densité, en kg/m**#
    :rtype: float
    :return: La viscosité cinématique en m**2/s
    :rtype: float
    :return: La liste des géométries de la canalisation
    :rtype: list
    :return: La liste des longueurs de chaque tronçon
    :rtype: list
    :return: La liste des rayons de chaque tronçon
    :rtype: list
    :return: 'oui' ou 'non' si l'utilisateur veut placer une pompe
    :rtype: str
    :return: La pression minimale à ne pas franchir, en Pa
    :rtype: float
    :return: La puissance de la pompe, en W
    :rtype: float
    :return: Le rendement de la pompe, entre 0 et 1
    :rtype: float
    """
    # On crée un objet YAML au sein duquel on charge une instance de LecteurYAML qui lit le fichier "deck.yamL"
    parser = LecteurYAML('yaml_exemple.yaml')
    # On exécute la fonction read_yaml() de notre objet LecteurYAML
    parsed_data = parser.read_yaml()

    for key, value in parsed_data.items():
        if key == 'nom du fluide':
            nom_fluide = value
        elif key == 'nombre de troncons':
            nbre_troncon = value
        elif key == 'materiau de la canalisation':
            materiau = value
        elif key == 'rugosite de la canalisation':
           rugosite = value
        elif key == 'forme de la section':
            forme = value
        elif key == 'diametre de la section':
            diametre = value
        elif key == 'vitesse initiale':
            vitesse_init = value
        elif key == 'debit initial':
            debit_init = value
        elif key == 'temperature initiale':
            temperature_init = value
        elif key == 'pression initiale':
            pression_init = value
        elif key == 'densite initiale':
            densite = value
        elif key == 'viscosite cinematique initiale':
            viscosite_cine = value
        elif key == 'liste des geometries de la canalisation':
            liste_geometrie = value
        elif key == 'liste des longueur des troncons':
            liste_longueur = value
        elif key == 'liste des rayons de courbure des troncons':
            liste_rayon = value
        elif key == 'placement de pompes':
            choix_pompe = value
        elif key == 'pression minimale':
            pression_min = value
        elif key == 'puissance de la pompe':
            puissance = value
        elif key == 'rendement de la pompe':
            rendement = value

    return nom_fluide, nbre_troncon, materiau, rugosite, forme, diametre, vitesse_init, debit_init, temperature_init, pression_init, densite, viscosite_cine, liste_geometrie, liste_longueur, liste_rayon, choix_pompe, pression_min, puissance, rendement

