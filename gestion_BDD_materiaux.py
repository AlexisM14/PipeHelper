import pandas as pd

# On enregistre la base de données dans df
df_materiaux = pd.read_excel('BDD_materiaux.xlsx')


def lister_les_materiaux():
    """Renvoie la liste des matériaux de la base de données"""
    return df_materiaux['Matériaux'].unique().tolist()


def afficher_materiaux():
    liste_materiaux = lister_les_materiaux()
    for i in range(len(liste_materiaux)):
        print(f"{i} - {liste_materiaux[i]}")


def recuperer_rugosite(nom_materiau):
    return df_materiaux['Rugosité'][df_materiaux['Matériaux'] == nom_materiau].tolist()[0]

def ajouter_materiaux():
    return True


def supprimer_materiaux():
    return True