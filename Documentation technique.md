
# Documentation technique – Projet ENEDIS Machine learning 2025

Ce document technique contient les différentes méthodes pour démarrer l'application ainsi que les schémas permettant de comprendre plus facilement son architecture.  
Plan du document :
- [Démarrer l'application](#demarr_app)
    - [Avec docker](#docker)
    - [en ligne](#en_ligne)
    - [en local](#local)
- [Architecture de l'application](#archi_app)
- [Schémas de l'application](#schema_app)
    - [Schéma 1 : schéma d'interactions du projet](#schema_1)
- [technologies utilisées](#techno)

## 0. Démarrer l'application <a name="demarr_app"></a>

Pour lancer l'application, vous avez le choix entre 3 méthodes :

#### 1. Avec Docker <a name="docker"></a>
   - Prérequis : Docker installé et lancé.
   - Télécharger l'image :
     ```bash
     docker pull boroto/shiny-app-m2:latest
     ```
   - Lancer le container :
     ```bash
     docker run -p 8000:8000 boroto/shiny-app-m2:latest
     ```
     Option alternative avec nommage du container :
     ```bash
     docker run -p 8000:8000 --name shiny-m2 shiny-app-m2-dpe
     ```
   - Arrêter et relancer le container si besoin :
     ```bash
     docker stop shiny-m2
     docker start shiny-m2
     ```

#### 2. En ligne <a name="en_ligne"></a>
   - Accéder à l'application via navigateur en copiant le lien suivant ou [ici](https://019a4bd3-a805-1edf-b315-108164c29847.share.connect.posit.cloud/) :  
     https://019a4bd3-a805-1edf-b315-108164c29847.share.connect.posit.cloud/
   - Cliquez sur le lien, attendez que l'API se remette en route (maximum une minute), et profitez de l'application !

#### 3. En local <a name="local"></a>
   - Cloner le repository :
     ```bash
     git clone https://github.com/OlivierBOROT/M2-Projet-ENEDIS/tree/main/Shiny
     cd Shiny
     ```
   - Créer un environnement virtuel :
     ```bash
     py -m venv nom_de_l_env
     ```
   - Installer les dépendances :
     ```bash
     pip install -r requirements.txt
     ```
   - Lancer l'application :
     - Sur VSCode : ouvrir `app.py` et cliquer sur **Run**.
     - Via terminal :
       ```bash
       py app.py
       ```

## 1. Architecture de l’application <a name="archi_app"></a>

L’application, disponible sur github [ici](https://github.com/OlivierBOROT/M2-Projet-ENEDIS), est composée de plusieurs modules Python répartis comme suit :

```
Architecture du projet                                   # Description
===================================================================================================
M2-Projet-ENEDIS/
├── api/                                                 # Répertoire de l'api FastAPI
├── Shiny/                                               # Répertoire de l'application Shiny
├── ml_donnees_finales/                                  # Répertoires des différents notebook de création de modèle
├── extraction_donnees/                                  # Répertoire du notebook d'extraction des données brutes
├── Documentation fonctionnelle.md                       # Documentation utilisateur
├── Documentation technique.md                           # Documentation technique
├── Rapport Machine Learning.md                          # Rapport sur le machine learning
├── README.md                                            # Readme
└── requirements.txt                                     # packages utilisés pour le fonctionnement de tout le projet.
```
note : un schéma bien plus détaillé de l'architecture des données vous attend en bas de ce rapport ([cliquez ici](#schema_detaille)).

## 2. Schémas de l'application <a name="schema_app"></a>
- [Schéma 1 : schéma d'interactions du projet](#schema_1)

#### Schéma 1 : schéma d'interactions du projet <a name="schema_1"></a>
![schéma impossible à charger, disponible dans le répertoire md_ressources](https://github.com/OlivierBOROT/M2-Projet-ENEDIS/blob/main/md_ressources/interaction_projet_M2_enedis.png)

note : une version plus détaillé de ce schéma est disponible en annexe [ici](#schema_1_detail) :


## Technologies utilisées <a name="techno"></a>

| Technologie | Logo | Description | Lien officiel |
|--------------|------|--------------|----------------|
| **Python** | <img src="https://www.python.org/static/community_logos/python-logo.png" width="60" height="60"> | Langage principal utilisé partout : pour le backend, scripts de data, API et Shiny. | [python.org](https://www.python.org/) |
| **FastAPI** | <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="60" height="60"> | Framework Python moderne et ultra-rapide pour créer l'API REST. | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) |
| **Shiny for Python** | <img src="https://shiny.posit.co/images/shiny-solo.png" width="60" height="60"> | Framework pour construire l'interface web interactive. | [posit.co/shiny](https://shiny.posit.co/) |
| **Docker** | <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Docker_Logo.svg/500px-Docker_Logo.svg.png" width="60" height="60"> | Conteneurisation pour exécuter l’application sur n’importe quel système. | [docker.com](https://www.docker.com/) |
| **Pandas** | <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/langfr-330px-Pandas_logo.svg.png" width="60" height="60"> | Package python pour la manipulation et analyse des données. | [pandas.pydata.org](https://pandas.pydata.org/) |
| **Plotly** | <img src="https://images.plot.ly/logo/new-branding/plotly-logomark.png" width="60" height="60"> | Visualisations interactives et graphiques de l'appli Shiny. | [plotly.com](https://plotly.com/) |
| **Folium** | <img src="https://python-visualization.github.io/folium/latest/_images/folium_logo.png" width="60" height="60"> | Création de cartes interactives sur l'appli Shiny. | [python-visualization.github.io/folium](https://python-visualization.github.io/folium/) |
| **Scikit-learn** | <img src="https://scikit-learn.org/stable/_static/scikit-learn-logo-small.png" width="60" height="60"> | Bibliothèque de machine learning. | [scikit-learn.org](https://scikit-learn.org/) |
| **Jupyter Notebook** | <img src="https://jupyter.org/assets/homepage/main-logo.svg" width="60" height="60"> | Notebook interactif pour exploration et analyses de données. | [jupyter.org](https://jupyter.org/) |

## Annexes

<a name="schema_detaille"></a>
schéma détaillé de l'architecture du projet


```
Architecture du projet (détaillé)                        # Description
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
├── Rapport Machine Learning.md                          # Rapport sur le machine learning
├── README.md                                            # Readme
└── requirements.txt                                     # packages utilisés pour le fonctionnement de tout le projet.
```

<a name="schema_1_detail"></a>
schéma d'interactions du projet (détaillé)

![schéma impossible à charger, disponible dans le répertoire md_ressources](https://github.com/OlivierBOROT/M2-Projet-ENEDIS/blob/main/md_ressources/interaction_projet_M2_enedis_detaille.png)