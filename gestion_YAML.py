# On commence par importer le fichier qui contient notre classe LecteurYAML
from LecteurYAML import LecteurYAML
import os


def get_name_yaml():
    nom = input("--> ")
    while not os.path.exists(nom):
        print(" Le fichier indiqué n'existe pas, entrez le nom du fichier sous la forme : [mon_fichier.txt]")
        nom = input("--> ")
    return nom


def get_info_yaml(nom):
    # On crée un objet YAML au sein duquel on charge une instance de LecteurYAML qui lit le fichier "deck.yamL"
    parser = LecteurYAML('yaml_exemple.yaml')
    # On exécute la fonction read_yaml() de notre objet LecteurYAML
    parsed_data = parser.read_yaml()

    # nom_fluide, nbre_troncon, materiau, rugosite, forme, diametre, vitesse_init, debit_init, temperature_init, pression_init, densite, viscosite_cine, liste_geometrie, liste_longueur, liste_rayon, choix_pompe, pression_min, puissance, rendement = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

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

