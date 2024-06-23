"""Ce script définit toutes les classes qui seront utiles au programme"""


class Troncon:
    # Classe Variable
    species = "Canine"

    # Méthode constructeur
    def __init__(self):
        self.liste_attributs = []

    def ajouter_attribut(self, attribut):
        self.liste_attributs.append(attribut)

