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

    # GENERAL
    @reactive.calc
    def dataset():
        """Retourne une copie du DataFrame principal pour usage réactif."""
        return df.copy()

    # Préparation des choix non réactifs pour la mise à jour de l'UI (DPE)
    choices_list = df['periode_construction'].unique().tolist()
    choices_list = [c for c in choices_list if pd.notna(c)]
    choices_list.sort()
    dpe_choices = ["Toutes"] + choices_list

    # ACCUEIL
    md = setup_accueil(session)

    # CONTEXTE
    setup_donnees(input, output, session, dataset)
    setup_rapports(input, output, session)

    # VISUALISATION

    # VISUALISATION : GRAPHS
    setup_graphs(input, output, session, dataset, dpe_choices)

    # VISUALISATION : CARTO
    setup_carto(input, output, session, dataset)

    # PREDICTION
    # ...