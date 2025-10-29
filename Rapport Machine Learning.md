Rapport de Machine Learning- Projet Enedis
===========================================


I.	Section Contexte & Méthodologie
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



II.	Section Résultats & Métriques
====================================


III.	Section Interprétation & Limites
===========================================
