"""
File: LecteurYAML.py
Author: Alexis Markiewicz
Date: 2024-07-08
Description: Ce script permet de définir la classe qui permet d'utiliser des fichiers .yaml.
Fichier repris du cours MGA802
"""

# Imports
import yaml


# Définition de la classe
class LecteurYAML:
    def __init__(self, file_path):
        """Méthode constructeur
        """
        self.file_path = file_path

    def read_yaml(self):
        """Cette fonction permet de lire le fichier .yaml

        :return: dictionnaire associant chaque valeur à sa clé
        :rtype: dict
        """
        with open(self.file_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
                return data
            except yaml.YAMLError as e:
                print(f"Error reading YAML file: {e}")