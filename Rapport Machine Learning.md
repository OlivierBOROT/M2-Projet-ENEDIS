Rapport de Machine Learning- Projet Enedis
===========================================


# I.	Section Contexte & Méthodologie
----------------------------------------
# A.	Contexte : 
Le présent projet a été réalisé dans le cadre du cours « Python Machine Learning » donné par Anthony SARDELLITTI au sein du Master 2 SISE de l’Université Lumière Lyon2.
Ce projet est inspiré par le challenge proposé par la société Enedis, via la plateforme data.gouv.fr.
L’objectif du projet est la création d’une application d’estimation du score DPE d’un logement et de sa consommation énergétique.
Cette estimation sera réalisée à l’aide d’un modèle de Machine Learning, entraîné et testé à partir des données issues des bases de données de l’ADEME.
Nous commencerons par détailler les concepts et données exploiter avant d’aborder la méthodologie retenue.
## 1.	Concepts
*	Le Diagnostic de Performance Energétique, ou DPE : 
Le Diagnostic de Performance énergétique ou DPE, est un outil d’évaluation de la performance énergétique d’un logement ou d’un bâtiment.
Il est à noter que, dans le projet présent, nous ne nous intéresserons qu’au DPE applicable aux logements particuliers. Nous mettrons donc de côté les DPE spécifique à des bâtiments entiers (couvrant donc les zones communes) ou les bâtiments à usage tertiaire.
Le diagnostic se fonde sur l’évaluation de la consommation d’énergie primaire/m² et /an du logement, évaluation basée uniquement sur les caractéristiques structurelles du logement concerné.
Suite à l’arrêté du 8 octobre 2021 modifiant la méthode de calcul et les modalités d’établissement du diagnostic de performance énergétique, l’énergie primaire évaluée comme nécessaire au maintien du confort thermique du logement est évaluée en tant que quantité d’énergie agrégée sur les 5 consommations : chauffage, eau chaude sanitaire, refroidissement, éclairage et auxiliaire. Il est à noter que :
  La valeur « éclairage » est déduite, lors du calcul du score, de la surface du logement, de la zone climatique dans laquelle se situe le logement et de constantes admises dans la réglementation. Elle ne découle pas d’observations du réel.
	La valeur « auxiliaire » comprend uniquement les consommations des appareils contribuant au confort thermique et climatique qui ne seraient inclus dans les catégories précédentes, soit les éléments de ventilation et/ou de pompes. Elle n’inclut aucunement les consommations liées à l’électroménager ou à d’autres usages.
*	Energie primaire vs énergie finale : 
L’énergie finale correspond à la quantité d’énergie effectivement livrée et consommée par l’utilisateur final. En termes de consommation électrique, par exemple, elle correspond au montant, en kWh, figurant sur la facture du fournisseur d’électricité.

L’énergie primaire quant à elle, correspond à la quantité totale d’énergie mobilisée par l’acte de consommation, soit l’énergie finale, effectivement consommée, mais augmentée par les quantités d’énergie mobilisées pour le transport, la distribution, le stockage, la transformation et la production de celle-ci.
La distinction est importante puisque le DPE évalue l’énergie primaire consommée par le logement et non l’énergie finale.
Il est à noter que la quantité d’énergie primaire est déduite à partir de la quantité finale d’énergie à laquelle sont appliqués des coefficients en fonction des type de sources d’énergie exploitées par le logement : électricité, bois, fioul, gaz… Ces coefficients sont des constantes, fixées réglementairement après analyse du cycle de vie d’un kW depuis sa production jusqu’à consommation par l’utilisateur final.
La distinction est particulièrement importante puisque le score du DPE est fondé sur la consommation évaluée en énergie primaire.
Par conséquent le process de définition d’une étiquette DPE suit le déroulé suivant : estimation de la consommation en énergie finale du logement, basée sur les caractéristiques structurelles de celui-ci et sur des standards de consommation=> conversion de cette estimation en énergie primaire par le biais de coefficients induits par les sources d’énergie utilisées=> confrontation de cette estimation à l’échelle de score en KW/m²et /an pour la définition de l’étiquette du DPE.

*	Agence de l’environnement et de la maîtrise de l’énergie,  ADEME :
Agence fondée en 1990 de la fusion entre 3 agences gouvernementales, l’ADEME a depuis 2011, en plus de ses missions historiques, pour rôle de réceptionner et enregistrer tous les DPE réalisés.
Cet enregistrement est par ailleurs une des conditions de validité du diagnostic (cf Décret n°2011-807 du 5 juillet 2011).
Cette collecte et enregistrement ont donné lieu à la naissance de l’observatoire des DPE, permettant d’agréger, comparer, analyser et extraire les données issues de l’ensemble des DPE réalisés depuis 2011.
C’est cette exhaustivité de la base qui conduit l’observatoire de l’ADEME à être notre principale source de données pour ce projet.

## 2.	Données
Comme précisé plus haut, la consommation énergétique du logement est évaluée en tant que quantité d’énergie agrégée sur les 5 consommations, à partir des qualités structurelles du bâti du logement.

Ainsi seules les données correspondant aux caractéristiques structurelles du bâtiment et celles permettant de tenir compte de l’évolution des matériaux et des techniques dans l’industrie du bâtiment seront retenues pour l’entraînement du modèle de machine learning, afin de s’approcher au plus près des conditions de calcul.

Autre modification apportée par l’arrêté du 8 octobre 2021, les diagnostics établis avant le 1er juillet 2021 ne sont plus valides depuis le 31 décembre 2024. Les diagnostics réalisés à compter du 1er juillet 2021 ont en revanche une durée de validité de dix ans.
Compte tenu de la date à laquelle ce projet est réalisé (d’octobre à novembre 2025) seules les données relatives aux DPE réalisés après le 1er juillet 2021 seront prises en compte.

Afin de circonscrire le périmètre de l’évaluation du DPE, un choix a été fait de n’observer et prédire que les DPE établis sur le territoire Auvergne Rhône Alpes, celui-ci présentant par ailleurs une vaste source de données avec d’importantes variations dans les DPE.
En effet, la région, comparativement à d’autres régions plus littorales ou plus au Nord du pays, a été assez peu impactée par les bombardements et destructions massives de la Seconde Guerre Mondiale, permettant une plus importante conservation et présence de bâtiments datant d’avant 1948. D’autre part, la région concentre 3 grands centres de gravité métropolitains : Lyon, Grenoble et Clermont-Ferrand. Cette attractivité des villes et cette concentration de main d’œuvre et de capitaux en fait une région avec une importante activité de construction et de rénovation.

# B. Méthodologie 
Dans un premier temps, l’ensemble du processus de prédiction a été testé avec un modèle RandomForestRegressor, incluant la sélection des variables explicatives, l’imputation des valeurs manquantes, l’encodage des variables catégorielles et la transformation logarithmique de la cible. Ce modèle a permis de vérifier la faisabilité de la tâche et d’obtenir des résultats de référence. Après exploration d’autres algorithmes et bibliothèques, le modèle XGBoost Regressor a été retenu comme solution finale, offrant de meilleures performances en termes de précision et de généralisation tout en restant robuste face à la structure des données. L’ensemble du pipeline de préparation des données a été conservé pour l’entraînement du modèle XGBoost optimisé.
# II. Section Machine Learning - Classification
## 1. Préparation et échantillonnage des données

Le fichier source `donnees_finales.csv` a été importé puis échantillonné à **700 000 lignes** pour réduire la taille du jeu de données et accélérer le traitement.

Les variables explicatives retenues sont :

- 'qualite_isolation_murs'
- 'type_batiment'
- 'type_installation_ecs'
- 'type_energie_principale_chauffage'
- 'qualite_isolation_plancher_bas'
- 'type_installation_chauffage'
- 'surface_habitable_logement'
- 'hauteur_sous_plafond'
- 'nombre_niveau_logement'
- 'isolation_toiture'
- 'type_generateur_n1_ecs_n1'
- 'type_generateur_chauffage_principal'
- 'periode_construction'

Les valeurs manquantes ont été imputées :

- Moyenne pour les variables numériques  
- Valeur la plus fréquente pour les variables catégorielles

Les variables catégorielles ont ensuite été encodées par la méthode **One-Hot Encoding** (`pd.get_dummies`), générant **65 variables explicatives**.

Répartition initiale des étiquettes DPE :

| Classe | Proportion |
|--------|-------------|
| C | 31.6 % |
| D | 28.9 % |
| E | 19.1 % |
| F | 7.8 % |
| G | 5.6 % |
| B | 4.4 % |
| A | 2.7 % |

Afin de compenser ce déséquilibre, la méthode **SMOTE** a été appliquée, produisant un ensemble d’entraînement équilibré entre les 7 classes (A à G).

Les données ont été divisées selon un ratio :

- **70 %** pour l’entraînement  
- **30 %** pour le test  


## 2. Entraînement initial

Un premier modèle **XGBoost** a été entraîné sur les données rééchantillonnées.  
Les paramètres de base utilisés incluaient :

- `n_estimators = 200`  
- `max_depth = 8`  
- `learning_rate = 0.1`  
- `subsample = 0.8`  
- `colsample_bytree = 0.8`  

Le modèle a ensuite été évalué sur le jeu de test.

## 3. Résultats du modèle initial

Les performances obtenues sur le jeu de test sont les suivantes :

- **Accuracy globale : 0.477 (≈ 48 %)**  
- **Précision / Rappel / F1-score :**
  - Les classes intermédiaires **C**, **D** et **E** sont les mieux prédites.  
  - Les classes extrêmes (**A**, **G**) montrent des performances correctes compte tenu de leur rareté.  
  - La classe **F** reste difficile à identifier (f1-score ≈ 0.18).  

Une matrice de confusion montre que les erreurs les plus fréquentes se produisent entre classes voisines (D ↔ E, E ↔ F).


## 4. Optimisation du modèle

Pour améliorer la performance du modèle initial, une **optimisation d’hyperparamètres** a été effectuée via `RandomizedSearchCV`.

### Meilleurs paramètres trouvés

- `n_estimators = 150`  
- `max_depth = 8`  
- `learning_rate = 0.2`  
- `subsample = 0.8`  
- `colsample_bytree = 0.9`


## 5. Résultats du modèle optimisé

**Accuracy globale : 0.542 (≈ 54 %)**

Précision / Rappel / F1-score par classe :

Les classes intermédiaires C, D et E restent les mieux prédites, avec des f1-scores autour de 0.54 à 0.70.

Les classes minoritaires ou extrêmes (A, B, F, G) présentent des performances plus modestes, bien que la classe A atteigne un f1-score de 0.73.

La classe F demeure la plus difficile à identifier (f1-score ≈ 0.26).

La matrice de confusion confirme que les erreurs se produisent principalement entre classes voisines, notamment D ↔ E et E ↔ F, ce qui est cohérent avec la proximité des étiquettes de DPE.

## 7. Sauvegarde du modèle

Le modèle optimisé a été sauvegardé au format `joblib` sous le nom :

> `modele_dpe_xgb2.pkl`

Ce fichier peut être directement réutilisé pour une application d’estimation automatique du DPE.

## 8. Interprétation des résultats

L’analyse des performances du modèle XGBoost met en évidence une bonne cohérence globale entre les prédictions et les étiquettes réelles du DPE. Le modèle parvient à distinguer les profils énergétiques typiques à partir des caractéristiques structurelles du bâti, tout en conservant une certaine difficulté à différencier les classes les plus proches sur l’échelle énergétique.

Les classes centrales sont globalement bien captées, traduisant la capacité du modèle à modéliser les comportements majoritaires présents dans les données. À l’inverse, les classes extrêmes ou peu représentées tendent à être partiellement assimilées à leurs voisines.

La structure des erreurs observée dans la matrice de confusion reflète cette continuité naturelle des niveaux de performance énergétique : les logements situés aux frontières entre deux classes (par exemple D et E) présentent souvent des caractéristiques similaires, rendant leur classification plus incertaine.

Dans l’ensemble, le modèle capture correctement les grandes tendances de la consommation énergétique et offre une base solide pour une estimation automatisée du DPE, tout en laissant entrevoir des axes d’amélioration.


# III. Section Machine Learning - Régression

### 1. Variables explicatives et cible
- Cible : consommation énergétique sur 5 usages (`conso_5_usages_ef`)  
- Variables explicatives utilisées :  
  - 'qualite_isolation_murs'
  - 'type_batiment'
  - 'type_installation_ecs'
  - 'type_energie_principale_chauffage'
  - 'qualite_isolation_plancher_bas'
  - 'type_installation_chauffage'
  - 'surface_habitable_logement'
  - 'hauteur_sous_plafond'
  - 'nombre_niveau_logement'
  - 'isolation_toiture'
  - 'type_generateur_n1_ecs_n1'
  - 'type_generateur_chauffage_principal
  - 'periode_construction'
  - 'code_postal_ban'
- Transformation logarithmique appliquée (`log1p`) pour stabiliser la variance  
- Variables catégorielles encodées par One-Hot Encoding  
- 66 variables explicatives après encodage  

### 2. Division train/test
- 70 % pour l’entraînement, 30 % pour le test  
- Pas de stratification nécessaire pour la régression  
- Jeu d’entraînement : 490 000 lignes, test : 210 000 lignes  

### 3. Entraînement du modèle XGBoost Regressor
- Modèle de base : `XGBRegressor`  
- Paramètres initiaux : n_estimators = 300, max_depth = 8, learning_rate = 0.1, subsample = 0.8, colsample_bytree=0.8, random_state=42
- Entraînement effectué sur le jeu rééchantillonné  

### 4. Résultats du modèle XGBoost Regressor initial
- Mean Squared Error (MSE) : 1 553 460 999,55  
- Root Mean Squared Error (RMSE) : 39 414 kWh  
- Coefficient de détermination (R²) : 0,449  

  **Interprétation :**
- Le RMSE indique qu'en moyenne, les prédictions du modèle diffèrent d'environ 39 414 kWh par rapport aux valeurs réelles.  
- Le R² de 0,449 signifie que le modèle explique environ 45 % de la variance totale de la consommation énergétique.  
- Ces résultats montrent que le modèle capture partiellement la structure des données, mais des marges d'amélioration restent possibles, notamment par l’optimisation des hyperparamètres.
### 5. Optimisation des hyperparamètres
- Recherche aléatoire avec validation croisée (RandomizedSearchCV) sur 20 combinaisons  
- Paramètres testés :  
  - n_estimators : [100, 200, 300]  
  - max_depth : [6, 10, 15]  
  - learning_rate : [0.01, 0.05, 0.1]  
  - subsample : [0.6, 0.8, 1.0]  
  - colsample_bytree : [0.6, 0.8, 1.0]  
  - min_child_weight : [1, 5, 10]  
- Meilleurs paramètres trouvés :  
  - n_estimators = 200  
  - max_depth = 15  
  - learning_rate = 0.1  
  - subsample = 1.0  
  - colsample_bytree = 0.8  
  - min_child_weight = 1  

### 6. Évaluation du modèle optimisé
- Prédiction sur le jeu de test : 210 000 lignes  
- Conversion inverse du logarithme (`expm1`) pour interpréter en kWh réels  
- Métriques obtenues :  
  - Mean Squared Error (MSE) : 1027647107.16  
  - Root Mean Squared Error (RMSE) : 32056.94 kWh  
  - Coefficient de détermination (R²) : 0.580  
- Interprétation :  
  - Modèle reproduit de manière satisfaisante la consommation énergétique globale  
  - Prévisions proches des valeurs réelles, cohérence générale des tendances  

### 7. Sauvegarde du modèle
- Modèle optimisé enregistré via `joblib`,  `modele_conso_xgb_opt2.pkl`  
- Ce fichier peut être directement réutilisé pour prédiction automatique de la consommation énergétique

### 8. Interprétation des résultats
Le modèle XGBoost optimisé parvient à reproduire les variations globales de la consommation énergétique des logements.
Les prédictions suivent les tendances générales observées dans les données réelles.

L’erreur moyenne (RMSE ≈ 32 000 kWh) indique une certaine variabilité résiduelle, principalement liée à la diversité des profils de bâtiments et aux incertitudes sur les données d’entrée.
Le coefficient de détermination (R² ≈ 0.58) montre que le modèle capture une part significative de la variance de la consommation énergétique, bien qu’une proportion non négligeable reste inexpliquée.

Les résultats suggèrent que le modèle appréhende correctement les facteurs structurels majeurs influençant la consommation (isolation, surface, type de chauffage, période de construction)

