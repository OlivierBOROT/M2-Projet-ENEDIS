# 🧠 M2-Projet-ENEDIS  
### Projet Python / Machine Learning — Master 2 SISE 2025  

English below : [here](#english_below).

---

## 🏠 Introduction  

Ce dépôt contient une application web **Shiny for Python** permettant à l'utilisateur de :  
- **Évaluer la classe de Diagnostic de Performance Énergétique (DPE)** d’un logement 🏠  
- **Estimer la consommation énergétique associée** ⚡  
- **Visualiser les données** à travers des **indicateurs, cartes et graphiques interactifs** 📊  

> Le **Diagnostic de Performance Énergétique (DPE)** renseigne sur la performance énergétique et climatique d’un logement (étiquettes A à G), en évaluant sa consommation d’énergie et son impact en termes d’émissions de gaz à effet de serre.  
> Il est obligatoire lors de la vente ou de la mise en location d’un bien immobilier.  
>  
> ℹ️ Source : [Ministère de la Transition Écologique](https://www.ecologie.gouv.fr/politiques-publiques/diagnostic-performance-energetique-dpe)

L’objectif de cette application est donc de permettre à l’utilisateur de **prédire la classe DPE** de son logement, d’estimer sa **consommation énergétique**, et d’**explorer les données de l’ADEME** à l’aide de graphiques, cartes et indicateurs interactifs.

---

## 👩‍💻 Équipe de développement  
Projet réalisé par 4 étudiants du **Master 2 SISE — Université Lumière Lyon 2** :  
- **Olivier BOROT**  
- **Constantin REY-COQUAIS**  
- **Aya MECHERI**  
- **Anne-Camille VIAL**

---

## ⚙️ Installation
- [Avec docker](#docker)
- [en ligne](#en_ligne)
- [en local](#local)

#### 1. Avec Docker 🚢 <a name="docker"></a>
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

#### 2. En ligne 🌐<a name="en_ligne"></a>
   - Accéder à l'application via navigateur en copiant le lien suivant ou [ici](https://019a4bd3-a805-1edf-b315-108164c29847.share.connect.posit.cloud/) :  
     https://019a4bd3-a805-1edf-b315-108164c29847.share.connect.posit.cloud/
   - Cliquez sur le lien, attendez que l'API se remette en route (maximum une minute), et profitez de l'application !

#### 3. En local 💻<a name="local"></a>
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

---


## Architecture du projet:

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


## License:
license MIT classique voir license : [lien](https://github.com/OlivierBOROT/M2-Projet-ENEDIS/blob/main/LICENSE)

---


## English version <a name="english_below"></a>


## 🏠 Introduction  

This repository hosts a **Shiny for Python web application** that allows users to:
- **Predict the Energy Performance Certificate (DPE)** class of a appartment or a house 🏠  
- **Estimate the associated energy consumption** ⚡  
- **Explore data** through **interactive charts, maps, and indicators** 📊  


> The **Diagnostic de Performance Énergétique / Energy Performance Certificate (DPE)** informs on the energetic climatic performance of an accomodation (rated from A to G), by evaluating its energy consomption and his environmental impact.
> It is mandatory when selling or renting a property in France.
>  
> ℹ️ Source : [Ministère de la Transition Écologique](https://www.ecologie.gouv.fr/politiques-publiques/diagnostic-performance-energetique-dpe)


Our goal is to provide a user-friendly tool to predict DPE classes, estimate energy usage, and explore ADEME’s datasets via a visual interface.

---

## 👩‍💻 Developers
Developped by four **Master 2 SISE — Université Lumière Lyon 2** :  
- **Olivier BOROT**  
- **Constantin REY-COQUAIS**  
- **Aya MECHERI**  
- **Anne-Camille VIAL**

---

## ⚙️ Installation
- [with Docker](#docker_gb)
- [online](#en_ligne_gb)
- [locally](#local_gb)

#### 1. with Docker 🚢 <a name="docker_gb"></a>
   - Prerequisite: Docker installed and running.
   - Download the image:
     ```bash
     docker pull boroto/shiny-app-m2:latest
     ```
   - Run the container:
     ```bash
     docker run -p 8000:8000 boroto/shiny-app-m2:latest
     ```
     Alternative option with custom container name:
     ```bash
     docker run -p 8000:8000 --name shiny-m2 shiny-app-m2-dpe
     ```
   - Stop and restart the container if needed:
     ```bash
     docker stop shiny-m2
     docker start shiny-m2
     ```

#### 2. Online 🌐<a name="en_ligne_gb"></a>
   - Access the app through your browser using the following link or [here](https://019a4bd3-a805-1edf-b315-108164c29847.share.connect.posit.cloud/) :  
     https://019a4bd3-a805-1edf-b315-108164c29847.share.connect.posit.cloud/
   - Click the link, wait for the API to restart (up to one minute), and enjoy the application!

#### 3. Local installation 💻<a name="local_gb"></a>
   - Clone the repository:
     ```bash
     git clone https://github.com/OlivierBOROT/M2-Projet-ENEDIS/tree/main/Shiny
     cd Shiny
     ```
   - Create a virtual environment:
     ```bash
     py -m venv nom_de_l_env
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Launch the application:
     - In VSCode: open `app.py` and click Run.
     - From the terminal:
       ```bash
       py app.py
       ```

---


## Project structure:

```
Architecture du projet                                   # Description
===================================================================================================
M2-Projet-ENEDIS/
├── api/                                                 # FastAPI backend directory
├── Shiny/                                               # Shiny web application directory
├── ml_donnees_finales/                                  # Directory for model creation notebooks
├── extraction_donnees/                                  # Directory for raw data extraction notebook
├── Documentation fonctionnelle.md                       # User documentation
├── Documentation technique.md                           # Technical documentation
├── Rapport Machine Learning.md                          # Machine Learning report
├── README.md                                            # Readme
└── requirements.txt                                     Python packages required for the entire project.
```


## License:
license MIT classique voir license : [link](https://github.com/OlivierBOROT/M2-Projet-ENEDIS/blob/main/LICENSE)