import pandas as pd
from calculs import *


# On enregistre la base de données dans df
df_geometrie = pd.read_excel('BDD_geometrie.xlsx')

# On enregistre les différentes informations de chaque géométrie
liste_angle = df_geometrie.groupby('nom')['angle'].apply(list).reset_index()
liste_angle_te = liste_angle[liste_angle['nom'] == 'te']['angle'].tolist()[0]
liste_angle_deviation = liste_angle[liste_angle['nom'] == 'deviation']['angle'].tolist()[0]
liste_angle_agrandissement = liste_angle[liste_angle['nom'] == 'agrandissement']['angle'].tolist()[0]
liste_angle_retrecissement = liste_angle[liste_angle['nom'] == 'retrecissement']['angle'].tolist()[0]

liste_rapport = df_geometrie.groupby('nom')['rapport rayon diametre'].apply(list).reset_index()
liste_rapport_coude_droit = liste_rapport[liste_rapport['nom'] == 'coude droit']['rapport rayon diametre'].tolist()[0]

liste_rapport = df_geometrie.groupby('nom')['rapport rayon diametre'].apply(list).reset_index()
liste_rapport_coude = liste_rapport[liste_rapport['nom'] == 'coude']['rapport rayon diametre'].tolist()[0]


def recuperer_attribut_geo(geometrie, colonne):
    liste =  df_geometrie.groupby('nom')[colonne].apply(list).reset_index()
    return liste[liste['nom'] == geometrie][colonne].tolist()[0]


def trouver_nombre_apres(liste, nombre):
    """Trouve le plus petit élément de la liste, plus grand que nombre"""
    liste_triee = sorted(liste, reverse=True)
    nombre_apres = liste_triee[0]
    for i in liste_triee:
        if i > nombre:
            nombre_apres = i
    return nombre_apres


def trouver_nombre_avant(liste, nombre):
    """Trouve le plus grand élément de la liste, plus petit que nombre"""
    liste_triee = sorted(liste)
    nombre_avant = liste_triee[0]
    for i in liste_triee:
        if i < nombre:
            nombre_avant = i
    return nombre_avant


def recuperer_fourchette_geo(geometrie, colonne, nombre):
    liste_nombres = df_geometrie.groupby('nom')[colonne].apply(list).reset_index()
    liste_nombres_geometrie = liste_nombres[liste_nombres['nom'] == geometrie][colonne].tolist()[0]
    nombre_avant = trouver_nombre_avant(liste_nombres_geometrie, nombre)
    nombre_apres = trouver_nombre_apres(liste_nombres_geometrie, nombre)
    return nombre_avant, nombre_apres


# Définition de la fonction qui va calculer le coefficient de perte de charge via la base de données de géométries
def recuperer_coeff_perte_charge_singuliere(geometrie, angle, diametre_entree, diametre_sortie, rayon_courbure):
    df = df_geometrie
    if geometrie == 'coude':
        rapport_rsurd = rayon_courbure/diametre_entree

        # Si le rapport est déjà dans la table on l'utilise
        if rapport_rsurd in liste_rapport_coude:
            return df[(df['nom'] == 'coude') & (df['rapport rayon diametre'] == rapport_rsurd)]['zeta'].tolist()[0]
        # Sinon, il faut l'estimer en faisant un produit en croix
        else:
            rapport_precedent, rapport_suivant = recuperer_fourchette_geo(geometrie, 'rapport rayon diametre', rapport_rsurd)
            coef_precedent = df[(df['nom'] == 'coude') & (df['rapport rayon diametre'] == rapport_precedent)]['zeta'].tolist()[0]
            coef_suivant = df[(df['nom'] == 'coude') & (df['rapport rayon diametre'] == rapport_suivant)]['zeta'].tolist()[0]
            return coef_precedent + ((rapport_rsurd - rapport_precedent)/(rapport_suivant - rapport_precedent))*(coef_suivant - coef_precedent)

    elif geometrie == 'te':
        colonne = 'angle'

        # Si l'angle est déjà dans la table on l'utilise
        if angle in liste_angle_te:
            return df[(df['nom'] == geometrie) & (df[colonne] == angle)]['zeta'].tolist()[0]
        # Sinon il faut l'estimer en faisant un produit en croix
        else:
            angle_precedent, angle_suivant = recuperer_fourchette_geo(geometrie, colonne, angle)
            coef_precedent = df[(df['nom'] == geometrie) & (df[colonne] == angle_precedent)]['zeta'].tolist()[0]
            coef_suivant = df[(df['nom'] == geometrie) & (df[colonne] == angle_suivant)]['zeta'].tolist()[0]
            return coef_precedent + ((angle - angle_precedent) / (angle_suivant - angle_precedent)) * (
                        coef_suivant - coef_precedent)

    elif geometrie == 'coude droit':
        colonne = 'rapport rayon diametre'

        rapport_rsurd = rayon_courbure / diametre_entree
        # Si le rapport est déjà dans la table on l'utilise
        if rapport_rsurd in liste_rapport_coude_droit:
            return df[(df['nom'] == geometrie) & (df[colonne] == rapport_rsurd)]['zeta'].tolist()[0]
        # Sinon, il faut l'estimer en faisant un produit en croix
        else:
            rapport_precedent, rapport_suivant = recuperer_fourchette_geo(geometrie, colonne, rapport_rsurd)
            coef_precedent = df[(df['nom'] == geometrie) & (df[colonne] == rapport_precedent)]['zeta'].tolist()[0]
            coef_suivant = df[(df['nom'] == geometrie) & (df[colonne] == rapport_suivant)]['zeta'].tolist()[0]
            return coef_precedent + ((rapport_rsurd - rapport_precedent) / (rapport_suivant - rapport_precedent)) * (
                        coef_suivant - coef_precedent)

    elif geometrie == 'deviation':
        colonne = 'angle'

        # Si l'angle est déjà dans la table on l'utilise
        if angle in liste_angle_deviation:
            return df[(df['nom'] == geometrie) & (df[colonne] == angle)]['zeta'].tolist()[0]
        # Sinon il faut l'estimer en faisant un produit en croix
        else:
            angle_precedent, angle_suivant = recuperer_fourchette_geo(geometrie, colonne, angle)
            coef_precedent = df[(df['nom'] == geometrie) & (df[colonne] == angle_precedent)]['zeta'].tolist()[0]
            coef_suivant = df[(df['nom'] == geometrie) & (df[colonne] == angle_suivant)]['zeta'].tolist()[0]
            return coef_precedent + ((angle - angle_precedent) / (angle_suivant - angle_precedent)) * (
                    coef_suivant - coef_precedent)

    elif geometrie == 'agrandissement':
        colonne = 'angle'

        # Si l'angle est déjà dans la table on l'utilise
        if angle in liste_angle_agrandissement:
            return df[(df['nom'] == geometrie) & (df[colonne] == angle)]['zeta'].tolist()[0]
        # Sinon il faut l'estimer en faisant un produit en croix
        else:
            angle_precedent, angle_suivant = recuperer_fourchette_geo(geometrie, colonne, angle)
            coef_precedent = df[(df['nom'] == geometrie) & (df[colonne] == angle_precedent)]['zeta'].tolist()[0]
            coef_suivant = df[(df['nom'] == geometrie) & (df[colonne] == angle_suivant)]['zeta'].tolist()[0]
            return coef_precedent + ((angle - angle_precedent) / (angle_suivant - angle_precedent)) * (
                    coef_suivant - coef_precedent)

    elif geometrie == 'retrecissement':
        colonne = 'angle'

        # Si l'angle est déjà dans la table on l'utilise
        if angle in liste_angle_retrecissement:
            return df[(df['nom'] == geometrie) & (df[colonne] == angle)]['zeta'].tolist()[0]
        # Sinon il faut l'estimer en faisant un produit en croix
        else:
            angle_precedent, angle_suivant = recuperer_fourchette_geo(geometrie, colonne, angle)
            coef_precedent = df[(df['nom'] == geometrie) & (df[colonne] == angle_precedent)]['zeta'].tolist()[0]
            coef_suivant = df[(df['nom'] == geometrie) & (df[colonne] == angle_suivant)]['zeta'].tolist()[0]
            return coef_precedent + ((angle - angle_precedent) / (angle_suivant - angle_precedent)) * (
                    coef_suivant - coef_precedent)

    else:
        print("Géométrie non trouvée")
