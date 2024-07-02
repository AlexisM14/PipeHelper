import pandas as pd

# On enregistre la base de données dans df
df_fluide = pd.read_excel('BDD_fluides.xlsx')


def lister_fluides():
    """Renvoie la liste des fluides de la base de données"""
    return df_fluide['Nom fluide'].unique().tolist()


def afficher_fluide():
    """Affiche les différents fluides de la base de données"""
    liste_noms = lister_fluides()
    fluides = str(liste_noms[0])
    for i in liste_noms[1:]:
        fluides += ', '
        fluides += i
    print(fluides)


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


# def ajouter_densite(nom_fluide, temperature):
#     """Permet d'ajouter une densité au fluide dans la base de données pour une certaine température"""
#     return True
#
#
# def ajouter_viscosite(nom_fluide, temperature):
#     """Permet d'ajouter une viscosité au fluide dans la base de données pour une certaine température"""
#     return True
#
#
# def ajouter_fluides():
#     """Permet d'ajouter un fluide à la base de données"""
#     nom_fluide = input("Quel est le nom du fluide que vous voulez ajouter la base de données ?")
#     print("Quelle est la température du fluide que vous voulez ajouter, en K ?")
#     temperature = get_float_input()
#     reponse = 'non'
#     while reponse == 'non':
#         print(f"Vous voulez ajouter les propriétés du {nom_fluide} à {temperature} K ?")
#         reponse = get_element_liste_input(['oui', 'non'])
#         nom_fluide = input("Quel est le nom du fluide que vous voulez ajouter la base de données ?")
#         print("Quelle est la température du fluide que vous voulez ajouter ?")
#         temperature = get_float_input()
#
#     # On ajoute le nom et la température à la base de données puis la densité et la viscosité
#
#     ajouter_densite(nom_fluide, temperature)
#     ajouter_viscosite(nom_fluide, temperature)
#     return True
#
#
# def recuperer_densite(nom_fluide, temperature):
#     return 23,4
#
#
# def modifier_densite(nom_fluide, temperature):
#     """Permet de modifier une densité au fluide dans la base de données pour une certaine température"""
#     densite = recuperer_densite(nom_fluide, temperature)
#     print(f"La densité actuelle pour {nom_fluide} à {temperature} K est {densite} kg/m3, voulez vous la modifier ?")
#     reponse = get_element_liste_input(['oui', 'non'])
#     if reponse == 'oui':
#         print("Entrez la nouvelle densité en kg/m3")
#         nouvelle_densite = get_float_input('+')
#         print(f"La nouvelle densité sera donc {nouvelle_densite} kg/m3 ?")
#         confirmation = 'non'
#         while confirmation == 'non':
#             print("Entrez la nouvelle densité en kg/m3")
#             nouvelle_densite = get_float_input('+')
#             print(f"La nouvelle densité sera donc {nouvelle_densite} kg/m3 ?")
#             confirmation = get_element_liste_input(['oui', 'non'])
#         # on modifie la densite
#     else:
#         print(f"Vous sortez de la modification de la densité de {nom_fluide} à {temperature} K")
#
#
# def modifier_viscosite(nom_fluide, temperature):
#     """Permet de modifier une viscosité au fluide dans la base de données pour une certaine température"""
#     viscosite = recuperer_densite(nom_fluide, temperature)
#     print(f"La viscosité actuelle pour {nom_fluide} à {temperature} K est {viscosite} Pa.s, voulez vous la modifier ?")
#     reponse = get_element_liste_input(['oui', 'non'])
#     if reponse == 'oui':
#         print("Entrez la nouvelle viscosité en Pa.s")
#         nouvelle_viscosite = get_float_input('+')
#         print(f"La nouvelle viscosité sera donc {nouvelle_viscosite} Pa.s ?")
#         confirmation = 'non'
#         while confirmation == 'non':
#             print("Entrez la nouvelle viscosité en Pa.s")
#             nouvelle_viscosite = get_float_input('+')
#             print(f"La nouvelle viscosité sera donc {nouvelle_viscosite} Pa.s ?")
#             confirmation = get_element_liste_input(['oui', 'non'])
#         # on modifie la viscosite
#     else:
#         print(f"Vous sortez de la modification de la viscosité de {nom_fluide} à {temperature} K")
#
#
# def supprimer_fluides():
#     """Permet de supprimer un fluide de la base de données"""
#     return True