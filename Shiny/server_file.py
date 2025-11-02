import asyncio
import requests
import pandas as pd
from shiny import App, reactive, ui, render, Session
from pathlib import Path

from server.import_rapports import setup_rapports
from server.accueil import setup_accueil
from server.donnees import setup_donnees
from server.cartographie import setup_carto
from server.graphs import setup_graphs

here = Path(__file__).parent
DATA_PATH = here / "data/data.parquet"

def server(input, output, session):
    df = pd.read_parquet(DATA_PATH)
    
    # --- FILTRE PERMANENT : Exclure les immeubles (ROBUSTE) ---
    if 'type_batiment' in df.columns:
        # CONVERSION ET FILTRE ROBUSTE : Exclut 'immeuble' quelle que soit la casse
        df = df[df['type_batiment'].str.lower() != 'immeuble']
    # -----------------------------------------------------------
    
    # GENERAL
    @reactive.calc
    def dataset():
        """Retourne une copie du DataFrame principal (sans les immeubles) pour usage réactif."""
        return df.copy() 
    
    # Préparation des choix non réactifs pour la mise à jour de l'UI (Période)
    choices_list = df['periode_construction'].unique().tolist()
    choices_list = [c for c in choices_list if pd.notna(c)]
    choices_list.sort()
    dpe_choices = ["Toutes"] + choices_list

    # Préparation des choix non réactifs pour la mise à jour de l'UI (Énergie)
    choices_list_energie = df['type_energie_principale_chauffage'].unique().tolist()
    choices_list_energie = [c for c in choices_list_energie if pd.notna(c)]
    choices_list_energie.sort()
    energie_choices = ["Toutes"] + choices_list_energie
    
    # Préparation des choix pour le filtre Type de Bâtiment (G4)
    choices_list_logement = df['type_batiment'].unique().tolist()
    choices_list_logement = [c for c in choices_list_logement if pd.notna(c)]
    choices_list_logement.sort()
    logement_choices = ["Toutes"] + choices_list_logement # Contient Maison/Appartement

    # ACCUEIL
    md = setup_accueil(session)
    
    # CONTEXTE
    setup_donnees(input, output, session, dataset)
    setup_rapports(input, output, session)

    # VISUALISATION
    setup_graphs(input, output, session, dataset, dpe_choices, energie_choices, logement_choices) # NOUVEL ARGUMENT
    setup_carto(input, output, session)

    # PREDICTION
