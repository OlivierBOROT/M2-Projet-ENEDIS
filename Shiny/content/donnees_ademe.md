# Présentation de l’ADEME et des DPE

L’**ADEME** (Agence de la Transition Écologique) joue un rôle central dans la mise en œuvre des politiques publiques liées à l’énergie, au climat et à la rénovation des bâtiments. Parmi ses missions, elle assure la gestion, la diffusion et la valorisation des données relatives aux **Diagnostics de Performance Énergétique (DPE)**, un dispositif essentiel pour évaluer l’efficacité énergétique et l’impact environnemental des logements en France.  
Pour plus d’informations, consulter le [site officiel de l’ADEME](https://www.ademe.fr/).

Ici, nous allons nous intéresser uniquement au **DPE**. Le **Diagnostic de Performance Énergétique (DPE)** fournit une estimation normalisée de la **consommation d’énergie** et des **émissions de gaz à effet de serre** d’un bâtiment, à partir de ses caractéristiques physiques (surface, orientation, isolation, matériaux, menuiseries) et de ses équipements (chauffage, ventilation, eau chaude sanitaire, etc.).  
Depuis la **réforme du 1er juillet 2021**, le DPE a été profondément modernisé afin de devenir **centralisé et uniformisé** dans la réglementation de la rénovation énergétique.

L'API rend disponible deux jeux de données différents :

- **DPE Logements neufs** : s’applique aux bâtiments dont la construction est postérieure à juillet 2021, suivant la méthode réglementaire 3CL (Calcul des Consommations Conventionnelles des Logements).  
  - [Dataset ADEME DPE Logements neufs](https://data.ademe.fr/datasets/dpe02neuf)
- **DPE Logements existants** : concerne les logements construits avant cette date, également soumis à la méthode 3CL, désormais généralisée à tous les types de biens.  
  - [Dataset ADEME DPE Logements existants](https://data.ademe.fr/datasets/dpe03existant)

## Paramètres principaux

Pour les données ADEME sur les DPE, les colonnes principales sélectionnées parmi les ~300 disponibles sont les suivantes :  
(liste non exhaustive des variables que nous avons sélectionné)

- **etiquette_dpe** : étiquette énergétique du logement  
- **conso_5_usages_ef** : consommation énergétique selon 5 usages (chauffage, eau chaude, ventilation, éclairage, auxiliaires)  
- **type_batiment** : type de bâtiment (maison, appartement, etc.)  
- **surface_habitable_logement** : surface habitable du logement (m²)  
- **hauteur_sous_plafond** : hauteur sous plafond (m)  
- **annee_construction** : année de construction du bâtiment  
- **zone_climatique** : zone climatique du logement  
- **classe_altitude** : classe d’altitude du logement  
- **type_installation_chauffage** : type d’installation de chauffage  
- **type_generateur_chauffage_principal** : type de générateur pour le chauffage principal  
- **type_energie_principale_chauffage** : énergie principale utilisée pour le chauffage  
- **type_installation_ecs** : type d’installation pour l’eau chaude sanitaire  
- **type_generateur_n1_ecs_n1** : type de générateur pour l’eau chaude sanitaire  
- **type_generateur_froid** : type de générateur pour la climatisation / froid  
