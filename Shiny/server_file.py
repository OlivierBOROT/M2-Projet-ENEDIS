import asyncio
import requests
import pandas as pd
from shiny import App, reactive, ui, render, Session
from pathlib import Path

from server.import_rapports import setup_rapports
from server.accueil import setup_accueil
from server.donnees import setup_donnees
from server.cartographie import setup_carto

here = Path(__file__).parent
DATA_PATH = here / "data/data.parquet"

def server(input, output, session):
    df = pd.read_parquet(DATA_PATH)
    # GENERAL
    @reactive.calc
    def dataset():
        return df.copy() # au cas où

    # ACCUEIL
    md = setup_accueil(session)
    # CONTEXTE

    # CONTEXTE : donnees
    setup_donnees(input, output, session, dataset)

    # CONTEXTE : rapports
    setup_rapports(input, output, session)

    # VISUALISATION

    # VISUALISATION : KPI - Graphs

    # VISUALISATION : catrographie
    setup_carto(input, output, session)

    # PREDICTION
