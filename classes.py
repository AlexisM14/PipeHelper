"""Ce script définit toutes les classes qui seront utiles au programme"""


class Troncon:
    # Classe Variable
    species = "Canine"

    # Méthode constructeur
    def __init__(self, longueur, section, diametre, materiau, rugosite):
        self.long = longueur
        self.sect = section
        self.diam = diametre
        self.mat = materiau
        self.rug = rugosite

    # Méthode
    def bark(self):
        print("Woof!")