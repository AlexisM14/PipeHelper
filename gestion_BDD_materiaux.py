"""
File: gestion_BDD_materiaux.py
Author: Alexis Markiewicz
Date: 2024-07-08
Description: Ce script permet de définir des fonctions qui permettent de gérer la base de données "BDD_amteriaux.xlsx"
"""

# Imports
import pandas as pd

# On enregistre la base de données dans df
df_materiaux = pd.read_excel('Base_De_Donnees/BDD_materiaux.xlsx')


# Définition des fonctions
def lister_les_materiaux():
    """
    Cette fonction permet de liste le nom des matériaux de la base de données.

    Args:
        Aucun

    Returns:
        list : La liste des noms des matériaux
    """
    return df_materiaux['Matériaux'].unique().tolist()


def afficher_materiaux():
    """
    Cette fonction permet d'afficher le nom des matériaux de la base de données.

    Args:
        Aucun

    Returns:
        Aucun
    """
    liste_materiaux = lister_les_materiaux()
    for i in range(len(liste_materiaux)):
        print(f"{i} - {liste_materiaux[i]}")


def recuperer_rugosite(nom_materiau):
    """
    Cette fonction permet de récupérer la rugosité de 'nom_materiau' dans la base de données.

    Args:
        nom_materiau (str) : Le nom du matériau dans la base de données

    Returns:
        float : La rugosité du matériau 'nom_materiau'
    """
    return df_materiaux['Rugosité'][df_materiaux['Matériaux'] == nom_materiau].tolist()[0]
