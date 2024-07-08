"""
File: gestion_BDD_fluides.py
Author: Alexis Markiewicz
Date: 2024-07-08
Description: Ce script permet de définir des fonctions qui permettent de gérer la base de données "BDD_fluides.xlsx"
"""

# Imports
import pandas as pd

# On enregistre la base de données dans df
df_fluide = pd.read_excel('Base_De_Donnees/BDD_fluides.xlsx')


# Définition des fonctions
def lister_fluides():
    """
    Cette fonction renvoie la liste des noms des fluides de la base données.

    Args:
        Aucun

    Returns:
        list : Les noms de fluides de la base de données
    """
    return df_fluide['Nom fluide'].unique().tolist()


def afficher_fluide():
    """
    Cette procédure affiche le nom des fluides de la base données.

    Args:
        Aucun

    Returns:
        Aucun
    """
    liste_noms = lister_fluides()
    for i in range(len(liste_noms)):
        print(f"{i} - {liste_noms[i]}")


def trouver_nombre_apres(liste, nombre):
    """
    Cette fonction renvoie le plus petit nombre, plus grand que 'nombre' dans la liste.

    Args:
        liste (list) : La liste des nombres
        nombre (float) : Le nombre dont il faut trouver le nombre le plus proche avant lui dans la liste

    Returns:
        float : Le plus petit nombre, plus grand que 'nombre' dans la liste
    """
    # On trie la liste
    liste_triee = sorted(liste, reverse=True)
    nombre_apres = liste_triee[0]
    for i in liste_triee:
        if i > nombre:
            nombre_apres = i
    return nombre_apres


def trouver_nombre_avant(liste, nombre):
    """
    Cette fonction renvoie le plus grand nombre, plus petit que 'nombre' dans la liste.

    Args:
       liste (list) : La liste des nombres
       nombre (float) : Le nombre dont il faut trouver le nombre le plus proche avant lui dans la liste

    Returns:
       float : Le plus grand nombre, plus petit que 'nombre' dans la liste
   """
    liste_triee = sorted(liste)
    nombre_avant = liste_triee[0]
    for i in liste_triee:
        if i < nombre:
            nombre_avant = i
    return nombre_avant


def recuperer_fourchette_fluide(nom_fluide, colonne, nombre):
    """
    Cette fonction renvoie le nombre juste avant et juste après 'nombre', dans la colonne 'colonne', pour 'fluide'
    dans la base de données.

    Args:
       nom_fluide (str) : Le nom du fluide
       colonne (str) : La colonne dans laquelle chercher
       nombre (float) : Le nombre qu'on souhaite encadrer dans la colonne 'colonne'

    Returns:
       float : Le plus grand nombre, plus petit que nombre dans la liste
       float : Le plus petit nombre, plus grand que nombre dans la liste
   """
    liste_nombres = df_fluide.groupby('Nom fluide')[colonne].apply(list).reset_index()
    liste_nombres_geometrie = liste_nombres[liste_nombres['Nom fluide'] == nom_fluide][colonne].tolist()[0]
    nombre_avant = trouver_nombre_avant(liste_nombres_geometrie, nombre)
    nombre_apres = trouver_nombre_apres(liste_nombres_geometrie, nombre)
    return nombre_avant, nombre_apres


def recuperer_liste_temperature(nom_fluide):
    """
    Cette fonction renvoie la liste des températures pour 'nom_fluide' dans la base de données.

    Args:
       nom_fluide (str) : Le nom du fluide

    Returns:
       list : La liste des températures pour le fluide 'nom_fluides'
    """
    liste_temperature = df_fluide.groupby('Nom fluide')['Température'].apply(list).reset_index()
    return liste_temperature[liste_temperature['Nom fluide'] == nom_fluide]['Température'].tolist()[0]


def recuperer_valeur_fluide(nom_fluide, temperature, colonne):
    """
    Cette fonction renvoie la valeur du fluide 'nom_fluide' dans la colonne 'colonne', à la température 'temperature'.

    Args:
       nom_fluide (str) : Le nom du fluide
       temperature (float) : La température du fluide
       colonne (str) : La colonne ou chercher la valeur

    Returns:
       float : La valeur recherchée dans la colonne à la température
    """
    liste_temperature = recuperer_liste_temperature(nom_fluide)
    if temperature in liste_temperature:
        return df_fluide[colonne][(df_fluide['Nom fluide'] == nom_fluide) & (df_fluide['Température'] == temperature)].tolist()[0]
    else:
        temp_precedent, temp_suivant = recuperer_fourchette_fluide(nom_fluide, 'Température', temperature)
        valeur_precedent = df_fluide[colonne][(df_fluide['Nom fluide'] == nom_fluide) & (df_fluide['Température'] == temp_precedent)].tolist()[0]
        valeur_suivant = df_fluide[colonne][(df_fluide['Nom fluide'] == nom_fluide) & (df_fluide['Température'] == temp_suivant)].tolist()[0]
        return valeur_precedent + ((temperature - temp_precedent) / (temp_suivant - temp_precedent)) * (
                    valeur_suivant - valeur_precedent)
