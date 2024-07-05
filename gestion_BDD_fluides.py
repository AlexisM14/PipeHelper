import pandas as pd

# On enregistre la base de données dans df
df_fluide = pd.read_excel('Base_De_Donnees/BDD_fluides.xlsx')


def lister_fluides():
    """Renvoie la liste des fluides de la base de données"""
    return df_fluide['Nom fluide'].unique().tolist()


def afficher_fluide():
    """Affiche les différents fluides de la base de données"""
    liste_noms = lister_fluides()
    for i in range(len(liste_noms)):
        print(f"{i} - {liste_noms[i]}")


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


def recuperer_fourchette_fluide(nom_fluide, colonne, nombre):
    """Renvoie la valeur dans la colonne avant et après le nombre pour le nom_fluide"""
    liste_nombres = df_fluide.groupby('Nom fluide')[colonne].apply(list).reset_index()
    liste_nombres_geometrie = liste_nombres[liste_nombres['Nom fluide'] == nom_fluide][colonne].tolist()[0]
    nombre_avant = trouver_nombre_avant(liste_nombres_geometrie, nombre)
    nombre_apres = trouver_nombre_apres(liste_nombres_geometrie, nombre)
    return nombre_avant, nombre_apres


def recuperer_liste_temperature(nom_fluide):
    """Renvoie la liste des températures pour chaque fluide dans la BDD"""
    liste_temperature = df_fluide.groupby('Nom fluide')['Température'].apply(list).reset_index()
    return liste_temperature[liste_temperature['Nom fluide'] == nom_fluide]['Température'].tolist()[0]


def recuperer_valeur_fluide(nom_fluide, temperature, colonne):
    """Renvoie la valeur dans 'colonne' du 'nom_fluide' à 'température'"""
    liste_temperature = recuperer_liste_temperature(nom_fluide)
    if temperature in liste_temperature:
        return df_fluide[colonne][(df_fluide['Nom fluide'] == nom_fluide) & (df_fluide['Température'] == temperature)].tolist()[0]
    else:
        temp_precedent, temp_suivant = recuperer_fourchette_fluide(nom_fluide, 'Température', temperature)
        valeur_precedent = df_fluide[colonne][(df_fluide['Nom fluide'] == nom_fluide) & (df_fluide['Température'] == temp_precedent)].tolist()[0]
        valeur_suivant = df_fluide[colonne][(df_fluide['Nom fluide'] == nom_fluide) & (df_fluide['Température'] == temp_suivant)].tolist()[0]
        return valeur_precedent + ((temperature - temp_precedent) / (temp_suivant - temp_precedent)) * (
                    valeur_suivant - valeur_precedent)


def ajouter_fluide(nom_fluide, temperature, masse_volumique, viscosite_dynamique, viscosite_cinematique, chaleur_massique, conductivite_thermique, coefficient_dilatation):
    nouveau_fluide = {'Nom fluide': nom_fluide, 'Température': temperature, 'Masse volumique': masse_volumique, 'Viscosité dynamique': viscosite_dynamique, 'Viscosité cinématique': viscosite_cinematique, 'Chaleur massique': chaleur_massique, 'Conductivité thermique': conductivite_thermique, 'Coefficient de dilatation': coefficient_dilatation}
    df_fluide.append(nouveau_fluide, ignore_index=True)


def modifier_fluide(index, nom_fluide=None, temperature=None, masse_volumique=None, viscosite_dynamique=None, viscosite_cinematique=None, chaleur_massique=None, conductivite_thermique=None, coefficient_dilatation=None):
    if nom_fluide is not None:
        df_fluide.at[index, 'Nom fluide'] = nom_fluide
    if temperature is not None:
        df_fluide.at[index, 'Température'] = temperature
    if masse_volumique is not None:
        df_fluide.at[index, 'Masse volumique'] = masse_volumique
    if viscosite_dynamique is not None:
        df_fluide.at[index, 'Viscosité dynamique'] = viscosite_dynamique
    if viscosite_cinematique is not None:
        df_fluide.at[index, 'Viscosité cinématique'] = viscosite_cinematique
    if chaleur_massique is not None:
        df_fluide.at[index, 'Chaleur massique'] = chaleur_massique
    if conductivite_thermique is not None:
        df_fluide.at[index, 'Conductivité thermique'] = conductivite_thermique
    if coefficient_dilatation is not None:
        df_fluide.at[index, 'Coefficient de dilatation'] = coefficient_dilatation


def supprimer_fluide(index):
    df_fluide.drop(index).reset_index(drop=True)


