

from LecteurYAML import LecteurYAML
import os


def get_name_yaml():
    """
    Cette fonction permet de récupérer le nom du fichier .yaml

    Args :
        Aucun

    Returns :
        str : nom du fichier .yaml
    """
    nom = input("--> ")
    while not os.path.exists(nom):
        print(" Le fichier indiqué n'existe pas, entrez le nom du fichier sous la forme : [mon_fichier.txt]")
        nom = input("--> ")
    return nom


def get_info_yaml(nom):
    """
    Cette procédure permet de récupérer les informations du fichier .yaml

    Args :
        nom (str) : Le nom du fichier .yaml

    Returns :
        str : Le nom du fluide
        int : Le nombre de tronçons
        str : Le nom du matériau de la canalisation
        float : La rugosité de la canalisation, en m
        str : La forme de la section de la canalisation
        float : Le diamètre de la canalisation, en m
        float : La vitesse intiale, en m/s
        float : Le débit, m**3/s
        float : La température initiale, en °C
        float : La pression initiale, en Pa
        float : La densité, en kg/m**#
        float : La viscosité cinématique en m**2/s
        list : La liste des géométries de la canalisation
        list : La liste des longueurs de chaque tronçon
        list : La liste des rayons de chaque tronçon
        str : 'oui' ou 'non' si l'utilisateur veut placer une pompe
        float : La pression minimale à ne pas franchir, en Pa
        float : La puissance de la pompe, en W
        float : Le rendement de la pompe, entre 0 et 1
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

