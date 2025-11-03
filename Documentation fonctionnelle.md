# Comment utiliser l'application Greentech

La documentation ci-après a pour objectif d'accompagner l'utilisateur de l'application  Greentech dans la prise en main de celle-ci.
Elle détaillera les différents onglets de l'application et leurs fonctionnalités.


## Cartographie

Naviguez sur notre carte afin de prendre connaissance de la répartition géographique de la consommation énergétique moyenne, du nombre de logements ou des zones considérées comme "à rénover".
Pour cela vous pouvez sélectionner de visualiser ces informations par département, pour une vue plus globale du territoire, ou par code postal, afin de faire une analyse plus fine.

## Données

Cette page vous permet de consulter les données qui ont permis le développement de l'application et du modèle de prédiction utilisé par la suite.

Vous pourrez ainsi prendre connaissance du processus d'extraction et de traitement des données, leurs sources et avoir un aperçu de leur forme.


## Prédiction

Cette page vous permet de réaliser deux prédictions : l'étiquette DPE de votre logement et une estimation des besoins en consommation énergétique de celui-ci.
Pour cela, quelques étapes :
* sélectionnez l'élément que vous souhaitez prédire(DPE ou consommation énergétique)
* remplissez le formulaire concernant les caractéristiques de votre logement
*  appuyez sur "Soumettre".
*  
Quelques précisions sur les champs relatifs à l'isolation de votre plancher et de vos murs : 

Concernant l'isolation de votre plancher, une **"très bonne"** isolation correspond à la présence d'un autre logement ou d'un espace chauffé sous le vôtre; une **"bonne"** isolation correspond à la présence d'un sous-sol isolé ou d'un vide sanitaire sous le plancher de votre logement ; 
une isolation **"moyenne"** correspond à la présence d'un sous-sol ou vide sanitaire non isolé; et enfin une isolation **"insuffisante"** correspond au cas de figure où votre logement est construit en terre-plein.


Concernant l'isolation de votre plancher, une **"très bonne"** isolation correspond à une isolation réalisée il y a moins de 10 ans, une **"bonne"** isolation correspond à une isolation réalisée il y a entre 10 et 20 ans;
une isolation **"moyenne"** correspond à une isolation réalisée il y a plus de 20 ans; et enfin une isolation **"insuffisante"** correspond au cas de figure où aucune isolation n'a été réalisée.


## Graphs

Cette page vous permet d'accéder à des graphiques de représentation et de navigation des données relatives à la consommation d'énergie et au DPE

Graphique n°1 : la répartition des logements entre les différentes classes de DPE selon leur période de construction, ou tenter de répondre à la question : les maisons plus anciennes sont-elles plus ou moins efficaces énergétiquement? ; vous pouvez sélectionner la période de construction  qui vous intéresse et ainsi observer si des variations sont à constater dans la répartition des étiquettes de DPE.

Graphique n°2 : la représentation graphique de la consommation électrique d'un logement par m² et pan an, selon leurs étiquettes DPE ; vous pouvez constater ici la proportion de variation selon les différentes catégories, afin de saisir visuellement l'intérêt de ce diagnostic dans l'anticipation de la consommation énergétique d'un logement (et donc de la facture qui l'accompagne)

Graphique n°3 : la répartition en proportion des étiquettes DPE selon le type d'énergie de chauffage utilisée; évaluez ainsi l'impact potentiel de l'énergie utilisée pour votre chauffage sur l'attribution d'une étiquette DFPE ou d'une autre. Pour cela, sélectionnez simplement le type d'énergie qui vous intéresse dans la barre de filtre et observez.

Graphique n°4 : la courbe permet de représenter la variation des surfaces habitables moyennes selon les périodes de construction; connaître la consommation par m² est important, mais le niveau d'impact (économique et écologique) peut changer drastiquement en fonction de la surface concernée, c'est pourquoi il peut être inmportant d'observer les archétypes de surfaces concernés.


## Rapport

Cette page vous permettra d'accéder à la documentation sur la réalisation de cette application : 
* la documentation technique, qui vous renseignera notamment sur les technologies et packages requis pour utiliser et/ou modifier cette application
* le rapport de Machine Learning, qui vous permettra de comprendre les choix qui ont été faits dans le développement du modèle de prédiction de l'application
* une copie de la présente documentation, afin que celle-ci puisse être accessible à tout moment par les utilisateurs de l'application.
