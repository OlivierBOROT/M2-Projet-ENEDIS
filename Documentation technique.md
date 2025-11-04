
# Documentation technique – Projet ENEDIS Machine learning 2025

Ce document technique contient les différentes méthodes pour démarrer l'application ainsi que les schémas permettant de comprendre plus facilement son architecture.  
Plan du document :
- [Démarrer l'application](#0-démarrer-lapplication)
    - [Avec docker](#docker)
    - [en ligne](#en_ligne)
    - [en local](#local)
- Architecture de l'application
- Schémas de l'application
    - [Schéma 1 : schéma d'interactions du projet](#schema_1)
    - [Schéma 2 : schéma de l'architecture de l'application Shiny](#schema_2)
    - [Schéma 3 : schéma de l'architecture de l'API](#schema_3)

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
   - Cliquer sur le lien, attendre que l'API se remette en route (maximum une minute), et profitez de l'application !

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

## 1. Architecture de l’application

L’application, disponible sur github [ici](https://github.com/OlivierBOROT/M2-Projet-ENEDIS), est composée de plusieurs modules Python répartis comme suit :

```
Architecture du projet                                   Description
===================================================================================================
M2-Projet-ENEDIS/
├── api/                                                 # Répertoire de l'api FastAPI
├── Shiny/                                               # Répertoire de l'application Shiny
├── ml_donnees_finales/                                  # Répertoires des différents notebook de création de modèle
├── extraction_donnees/                                  # Répertoire du notebook d'extraction des données brutes
├── Documentation fonctionnelle.md                       # Documentation utilisateur
├── Documentation technique.md                           # Documentation technique
├── Rapport Machine Learning.md                          # Documentation générale
├── README.md                                            # Readme
└── requirements.txt                                     # packages utilisés pour le fonctionnement de tout le projet.
```
note : un schéma bien plus détaillé de l'architecture des données vous attend en bas de ce rapport ([cliquez ici](#schema_detaille)).

## 2. Schémas de l'application
- [Schéma 1 : schéma d'interactions du projet](#schema_1)
- [Schéma 2 : schéma de l'architecture de l'application Shiny](#schema_2)
- [Schéma 3 : schéma de l'architecture de l'API](#schema_3)

#### Schéma 1 : schéma d'interactions du projet <a name="schema_1"></a>
![Alt text](https://assets.digitalocean.com/articles/alligator/boo.svg "a title")

#### Schéma 2 : schéma de l'architecture de l'application Shiny <a name="schema_2"></a>
*ajouter le schéma ici*  

#### Schéma 3 : schéma de l'architecture de l'API <a name="schema_3"></a>
*ajouter le schéma ici*  



## Annexes

<a name="schema_detaille"></a>
schéma détaillé

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
├── Rapport Machine Learning.md                          # Documentation générale
├── README.md                                            # Readme
└── requirements.txt                                     # packages utilisés pour le fonctionnement de tout le projet.
```
