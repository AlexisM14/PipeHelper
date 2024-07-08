# Objectif du code 
Le programme permet d’étudier une canalisation, d’y calculer la distribution de pression et de
trouver les endroits où placer des pompes afin que la pression du fluide ne puisse descendre sous un
certain seuil. Ce programme peut s’exécuter de deux façons différentes. La première est d’entrer, à la
main, dans la console les paramètres de l’étude de la canalisation. La deuxième est d’utiliser un fichier
.yaml.

# Comment utiliser le code
Pour utiliser ce script, il suffit de :
- Télécharger le script
- Installer les librairies PyYAML 6.0.1, Matplotlib 3.9.0, Numpy 1.26.4, Openpyxl 3.1.3 et Pandas 2.2.2
- Lancer main.py
- Suivre les instructions données dans la console

Si vous avez du mal à utiliser le script, le fichier exemple_utilisation.pdf vous aidera.

# Stratégie adoptée pour la structure du code
Le code est décomposé en plusieurs fichiers : calculs.py, classes.y, gestion_BDD_fluides.py, gestion_BDD_geometries.py, gestion_BDD_materiaux.py, gestion_traces.py, gestion_YAML.py, LecteurYAML.py, verifications.py et main.py. Le code principal se situe dans main.py et fait appel aux autres fichiers du dossier.
Trois bases de données : "BDD_fluides.xlsx", "BDD_materiaux.xlsx" et "BDD_geometries.xlsx" sont fournies avec le code et permettent son éxécution. 

## Organigramme de la structure du code
Les différents fichiers du programme intéragissent entre eux selon l'organigramme ci-dessous :

![image](https://github.com/AlexisM14/PipeHelper/assets/169942060/cbc484e3-ece0-4a45-9d3b-2890e022bbec)

## Description des fichiers
### calculs.py
Ce fichier comporte tous les calculs de perte de charge utiles pour déterminer la distribution de pression dans la canalisation, pour cela 7 fonctions sont utilisées. 
Certaines fonctions utilisent les relations suivantes, vues en [1] et [2] : 

Le nombre de Reynolds : $Re = \frac{vD}{\nu}$

La relation vitesse-débit : $Q = vS$

Le coefficient de perte de charge régulière :  
- Si Re < 2000 :  
        $f_D = \frac{64}{Re}$  
- Si Re $\ge$ 2000 :  
        $A = -2log(\frac{\epsilon}{3.7D}+\frac{12}{Re})$  
        $B = -2log(\frac{\epsilon}{3.7D}+\frac{2.51A}{Re})$  
        $C = -2log(\frac{\epsilon}{3.7D}+\frac{2.51B}{Re})$  
        $f_D = (A-\frac{(B-A)^2}{C-2B+A})$  
  On a alors $\Lambda = f_D\frac{L}{D}$  
  
Le coefficient de perte de charge singulière : $\Lambda$ dépend des géométries rencontrées, il peut aller de 0.2 à 2 pour un coude à 90°, il faut se réferrer à la base de donnée "BDD_geometrie.xlsx"  

On a alors les pertes de charges singulières et régulières : $\Delta P = \Lambda \rho \frac{v^2}{2}$
 
avec : 
- v la vitesse
- D le diamètre
- $\nu$ la viscosité dynamique
- Q le débit
- S la surface
- $\rho$ la densité
- $\epsilon$ la rugosité     

On obtient alors les fonctions :
- **calculer_reynolds** : Cette fonction calcule le nombre de Reynolds dans la canalisation.
- **calculer_debit2vitesse** : Cette fonction convertit un débit en vitesse.
- **calculer_coef_perte_de_charge** : Cette fonction calcule le coefficient de perte de charge régulière, selon le nombre de Reynolds.
- **calculer_perte_reguliere** : Cette fonction calcule la différence de pression due aux pertes de charges régulières.
- **calculer_perte_chgt_brusque_section** : Cette fonction calcule la différence de pression due aux pertes de charges singulières causées par un changement de section brusque.
- **calculer_pression_sortie_pompe** : Cette fonction calcule la pression en sortie d'une pompe.
- **calculer_perte_singuliere** : Cette fonction calcule la différence de pression due aux pertes de charges singulières.


### classes.py
Ce fichier nous permet de définir deux classes : 

- **Troncon** : Cette classe permet de définir un tronçon d'une canalisation. Un objet Troncon est définit par des attributs tels que : sa longueur, section, diametre, materiau, rugosite, geometrie, courbure, fluide, vitesse, pression, temperature densite et viscosite.  Cette classe dispose de plusieurs fonctions permettant d'afficher, modifier, ajouter certains attributs et même de calculer le nombre de Reynolds et les pertes de charges de ce tronçon.
- **Canalisation** : Cette classe permet de définir une canalisation. Elle est en fait une liste de Troncon successifs. Elle dipose de plusieurs fonctions permettant de renvoyer, afficher ou modifier les attributs des tronçons successifs et de calculer la distribution de pression.
- 
### gestion_BDD_fluides.py
Ce fichier permet d'exploiter la base de données "BDD_fluides.xlsx". Cette BDD est basée sur [3] et se décompose en 8 colonnes : Nom fluide, Température, Masse volumique, Viscosité dynamique, Viscosité cinématique, Chaleur massique, Conductivité thermique et Coefficient de dilatation. Pour ajouter, modifier ou supprimer des fluides il faut directement modifier cette BDD. On définit alors les fonctions suivantes :

- **lister_fluides** : Cette fonction renvoie la liste des noms des fluides de la base données.
- **afficher_fluide** : Cette procédure affiche le nom des fluides de la base données.
- **trouver_nombre_apres** : Cette fonction renvoie le plus petit nombre, plus grand que 'nombre' dans la liste.
- **trouver_nombre_avant** : Cette fonction renvoie le plus grand nombre, plus petit que 'nombre' dans la liste
- **recuperer_fourchette_fluide** : Cette fonction renvoie le nombre juste avant et juste après 'nombre', dans la colonne 'colonne', pour 'fluide' dans la base de données
- **recuperer_liste_temperature** : Cette fonction renvoie la liste des températures pour 'nom_fluide' dans la base de données.
- **recuperer_valeur_fluide** : Cette fonction renvoie la valeur du fluide 'nom_fluide' dans la colonne 'colonne', à la température 'temperature'.

### gestion_BDD_geometries.py
Ce fichier permet d'exploiter la base de données "BDD_geometries.xlsx". Cette BDD est basée sur [4] se décompose en 5 colonnes : nom, rapport rayon diametre, angle, rapport diametre sortie entree et zeta. Pour ajouter, modifier ou supprimer des géométries il faut directement modifier cette BDD. On définit alors les fonctions suivantes :

- **recuperer_attribut_geo** : Cette fonction récupère une valeur pour la géométrie 'geometrie' dans la colonne 'colonne'.
- **recuperer_fourchette_geo** : Cette fonction renvoie le nombre juste avant et juste après 'nombre', dans la colonne 'colonne', pour 'fluide' dans la base de données.
- **recuperer_coeff_perte_charge_singuliere** : Cette fonction renvoie le coefficient de perte de charge singulière pour la géométrie, l'angle, le diamètre et le rayon de courbure donné.

### gestion_BDD_materiaux.py
Ce fichier permet d'exploiter la base de données "BDD_materiaux.xlsx". Cette BDD est basée sur [5] se décompose en 2 colonnes : Matériaux et Rugosité. Pour ajouter, modifier ou supprimer des matériaux il faut directement modifier cette BDD. On définit alors les fonctions suivantes :

- **lister_les_materiaux** : Cette fonction permet de liste le nom des matériaux de la base de données.
- **afficher_materiaux** : Cette fonction permet d'afficher le nom des matériaux de la base de données.
- **recuperer_rugosite** : Cette fonction permet de récupérer la rugosité de 'nom_materiau' dans la base de données.

### gestion_traces.py
Toutes les fonctions de tracé sont implémentés dans ce fichier, pour notre programme on a besoin de 4 fonctions : 

- **calculer_coordonnees_coude** : Cette fonction permet de calculer les coordonnées d'un coude.
- **calculer_coordonnees_guide** : Cette fonction permet de calculer les coordonnées d'une canalisation.
- **tracer_canalisations** : Cette procédure permet de tracer la canalisation.
- **tracer_pression_vitesse_1d** : Cette procédure permet de tracer les variations de pression et de vitesse le long de la canalisation.

### gestion_YANL.py
Les fonctions permettant de manipuler les fichiers .yaml sont implémentées dans ce fichier.

- **get_name_yaml** : Cette fonction permet de récupérer le nom du fichier .yaml.
- **get_info_yaml** : Cette procédure permet de récupérer les informations du fichier .yaml.

### LecteurYAML.py
Ce fichier permet d'implémenter une classe spéciale pour les fichier .yaml :

- **LecteurYAML** : Cette classe permet de définir un fichier .yaml à partir de son chemin d'exécution, elle possède une méthode permettant de lire le fichier. 

### verifications.py
Ce fichier permet d'implémenter les fonctions qui vériefiront que les données entrées par l'utilisateur sont correctes et correspondent bien à ce qui est attendu. On définit alors les fonctions suivantes :

- **get_float_input** : Cette fonction permet de récupérer un flottant, qu'a entré l'utilisateur.
- **get_int_input** : Cette fonction permet de récupérer un entier, qu'a entré l'utilisateur.
- **get_element_liste_input** : Cette fonction permet de récupérer un élément d'une liste, entré par l'utilisateur.
- **get_init_cond_input** : Cette fonction permet de récupérer les conditions initiales, entrées par l'utilisateur.
- **get_float_between_input** : Cette fonction permet de récupérer un flottant, entré par l'utilisateur, dans un intervalle.
- **get_int_between_input** : Cette fonction permet de récupérer un entier, entré par l'utilisateur, dans un intervalle.

### main.py
Ce fichier est le fichier principal du programme, il utilise les autres fichiers afin d'effectuer les calculs de pression, d'après les données entrées par l'utilisateur. On définit alors les fonctions : 

- **nettoyer_ecran** : Cette procédure permet de nettoyer la console.
- **choisir_materiaux_canalisation** : Cette fonction permet de récupérer le nom des matériaux composant la canalisation.
- **choisir_rugosite_canalisation** : Cette fon.ction permet de récupérer les rugosités de la canalisation.
- **choisir_geometrie_canalisatio** : Cette fonction permet de récupérer les géométries de la canalisation.
- **nchoisir_longueur_canalisation** : Cette fonction permet de récupérer les longueurs des géométries de la canalisation.
- **verifier_rapport_canalisation** : Cette fonction permet de vérifier que les rapports rayon de courbure / diametre des coudes sont bien couverts par la base de données.
- **verifier_dans_intervalle** : Cette fonction permet de vérifier qu'un nombre est bien dans un intervalle.
- **recuperer_index_plus_proche_inf** : Cette fonction permet de récupérer l'index du nombre le plus petit et le plus proche de 'nbre' dans une liste.
- **trouver_emplacement_pompe** : Cette fonction permet de récupérer l'index ou placer une pompe pour que la pression ne descende pas sous 'pression_min'.
- **placer_pompeinterface** : Cette procédure permet de tracer la distribution de pressions dans la canalisation, avec des ponmpes.
- **interface** : Cette procédure permet de lancer le programme.

# Références

- [1 - Nombre de Reynolds](https://fr.wikipedia.org/wiki/Nombre_de_Reynolds)
- [2 - Pertes de charge](https://fr.wikipedia.org/wiki/Perte_de_charge)
- [3 - Base de données des fluides](https://public.iutenligne.net/)
- [4 - Base de données des géométries](https://sibam89.fr/?p=1575)
- [5 - Base de données des matériaux](https://www.thermexcel.com/french/ressourc/pdc_line.htm)
