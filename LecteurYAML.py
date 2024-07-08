"""
File: LecteurYAML.py
Author: Alexis Markiewicz
Date: 2024-07-08
Description: Ce script permet de définir la classe qui permet d'utiliser des fichiers .yaml.
"""

# Imports
import yaml


# Définition de la classe
class LecteurYAML:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_yaml(self):
        """
        Cette fonction permet de lire le fichier .yaml

        Args :
            Aucun

        Returns :
            dict : dictionnaire associant chaque valeur à sa clé
        """
        with open(self.file_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
                return data
            except yaml.YAMLError as e:
                print(f"Error reading YAML file: {e}")