
# Documentation technique – Projet ENEDIS Machine learning 2025

/ petite introduction /

## 1. Architecture de l’application

L’application est composée de plusieurs modules Python répartis comme suit :


## Arborescence (extraite du dépôt)

Voici l'organisation du projet tel que sur le [repo github](https://github.com/OlivierBOROT/M2-Projet-ENEDIS):

```
Architecture du projet                                   Description
===================================================================================================
M2-Projet-ENEDIS/
├── api/                                                 # Répertoire de l'Api FastAPI
│ ├─ app/                                                # contient les différents modèles au format .pkl
│ ├─ core/                                               # paramètres / configuration de l'API
│ ├─ models/                                             # schémas de données utilisés par l'API
│ ├─ routes/                                             # répertoire des différentes branches (ie. model_download, model_list ...)
│ ├─ main.py                                             # fichier principal, gère les routes et l'application
│ └─ requirements.txt                                    # packages utilisés pour le fonctionnement de l'API
│
├── Shiny/                                               # Répertoire de l'application Shiny
│ ├─ content/                                            # contenu de certaines pages au format .md
│ ├─ data/                                               # jeu de données
│ ├─ maps/                                               # maps créé par l'utilisateur
│ ├─ pages/                                              # différentes pages
│ ├─ server/                                             # Logique serveur Shiny
│ ├─ www/                                                # images, schémas, style.css
│ ├─ app.py                                              # fichier principal, gère les appels aux pages et l'application
│ ├─ server_file.py                                      # logique "back-end" de Shiny, gère les appels aux fonctions
│ └─ requirements.txt                                    # packages utilisés pour le fonctionnement de l'application Shiny
│
├── ml_donnees_finales/                                  # Répertoires des différents notebook de création de modèle
│
├── extraction_donnees/                                  # Répertoire du notebook d'extraction des données brutes
│ ├─ Classes_API/                                        # Répertoire des classes d'extraction des données des API
│ ├─ Transformation_donnees/                             # Fonctions plus spécifiques utilisées dans le notebook main
│ ├─ data/                                               # Données récupérées
│ ├─ fonctions_supplémentaires/                          # fonctions pas utilisées dans le notebook
│ ├─ main.ipynb                                          # notebook du processus d'extraction des données
│ ├─ requirements.txt                                    # packages utilisés pour le fonctionnement du notebook d'extraction.
│ ├─ stop_words.py                                       # stop_words français
│ └─ variables_globales.py                               # variable DEBUG globale.
│
├── Documentation fonctionnelle.md                       # Documentation utilisateur
├── Documentation technique.md                           # Documentation technique
├── Rapport Machine Learning.md                          # Documentation générale
├── README.md                                            # Readme
└── requirements.txt                                     # packages utilisés pour le fonctionnement de tout le projet.
```


M2‑Projet‑ENEDIS/
│
├─ Shiny/ # Application Shiny (front‑end & UI)
│ ├─ app.py # Point d’entrée de l’application Shiny
│ ├─ ui/ # Fichiers UI (layout, composants Shiny)
│ └─ server/ # Logique serveur Shiny
├─ api/ # API REST (backend)
│ ├─ main.py # Lancement de l’API via FastAPI
│ ├─ routes.py # Définition des endpoints REST
│ └─ utils.py # Fonctions utilitaires pour l’API
├─ extraction_donnees/ # Pipeline d’extraction des données brutes
├─ ml_donnees_finales/ # Modèles, données finales prêtes à être utilisées
├─ requirements.txt # Liste de toutes les dépendances Python
├─ README.md # Présentation du projet et instructions d’installation
└─ Documentation technique.md # Ce document
/ schéma de l'architecture du code /
- comment l'appli shiny parle avec les autres
- comment 

/ presentation vite fait des requirements /

